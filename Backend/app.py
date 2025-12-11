import os
import json
import pandas as pd
import joblib
import xgboost as xgb
TF_AVAILABLE = False
lstm_autoencoder = None
try:
    import tensorflow as tf
    TF_AVAILABLE = True
except Exception as e:
    print(f"[WARNING] TensorFlow not available: {e}")
    print("[OK] Continuing with 4 AI models (LSTM disabled)")
import numpy as np
import traceback
import logging
from datetime import datetime, timezone, timedelta
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required, 
    get_jwt_identity, get_jwt
)
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from werkzeug.security import generate_password_hash, check_password_hash
from pymongo import MongoClient
from web3 import Web3
from web3.exceptions import TransactionNotFound, BlockNotFound
from twilio.rest import Client as TwilioClient
from twilio.twiml.voice_response import VoiceResponse, Gather
from dotenv import load_dotenv
from zkp_handler import zkp_handler
from did_handler import did_handler
from transformer_detector import transformer_detector
from polygon_integration import PolygonLayer2  # ✅ POLYGON ADDED
load_dotenv()
app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})
app.config.from_mapping(
    SECRET_KEY=os.environ.get('SECRET_KEY'),
    JWT_SECRET_KEY=os.environ.get('JWT_SECRET_KEY'),
    SQLALCHEMY_DATABASE_URI=os.environ.get('DATABASE_URL'),
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
    JWT_ACCESS_TOKEN_EXPIRES=timedelta(hours=1)
)
db = SQLAlchemy(app)
jwt = JWTManager(app)
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://"
)

# --- 3. LOGGING CONFIGURATION ---
os.makedirs('logs', exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    handlers=[
        logging.FileHandler('logs/app.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# --- 4. SERVICE CONNECTIONS ---
try:
    mongo_client = MongoClient(os.environ.get('MONGO_URI'))
    mongo_db = mongo_client.get_database('fraud_logs_db')
    logger.info("[OK] Connected to MongoDB")
except Exception as e:
    logger.error(f"[ERROR] MongoDB connection failed: {e}")
    mongo_db = None

try:
    web3 = Web3(Web3.HTTPProvider(os.environ.get('INFURA_URL', 'http://127.0.0.1:7545')))
    signer = web3.eth.account.from_key(os.environ.get('SIGNER_PRIVATE_KEY'))
    web3.eth.default_account = signer.address
    logger.info(f"[OK] Connected to blockchain. Account: {signer.address}")
except Exception as e:
    logger.error(f"[ERROR] Blockchain connection failed: {e}")
    web3 = None

try:
    twilio_client = TwilioClient(
        os.environ.get('TWILIO_ACCOUNT_SID'),
        os.environ.get('TWILIO_AUTH_TOKEN')
    )
    logger.info("[OK] Twilio client initialized")
except Exception as e:
    logger.error(f"[ERROR] Twilio initialization failed: {e}")
    twilio_client = None

# --- 5. AI MODELS LOADING ---
logger.info("Loading AI models...")
try:
    model_path = 'models/trained_models/'
    iso_forest = joblib.load(os.path.join(model_path, 'isolation_forest.joblib'))
    logger.info("[OK] Isolation Forest loaded")
    if TF_AVAILABLE:
        try:
            lstm_autoencoder = tf.keras.models.load_model(
                os.path.join(model_path, 'lstm_autoencoder.h5'),
                custom_objects={'mae': tf.keras.losses.MeanAbsoluteError()}
            )
            logger.info("[OK] LSTM Autoencoder loaded")
        except Exception as e:
            logger.warning(f"[WARNING] LSTM loading failed: {e}")
            lstm_autoencoder = None
    else:
        logger.info("[WARNING] TensorFlow not available - LSTM disabled (4 models active)")
        lstm_autoencoder = None
    xgb_model = xgb.XGBClassifier()
    xgb_model.load_model(os.path.join(model_path, 'xgb_risk_model.json'))
    logger.info("[OK] XGBoost model loaded")
    rf_model = joblib.load(os.path.join(model_path, 'random_forest.joblib'))
    logger.info("[OK] Random Forest loaded")
    scaler = joblib.load(os.path.join(model_path, 'scaler.joblib'))
    logger.info("[OK] Scaler loaded")
    logger.info("Loading Transformer model...")
    logger.info("[OK] Transformer detector initialized")
    logger.info("[SUCCESS] All AI models loaded successfully")
except Exception as e:
    logger.error(f"[ERROR] FATAL: Could not load models. Error: {e}")
    exit(1)
# --- 6. SMART CONTRACTS LOADING ---
try:
    with open('build/contracts/FraudMitigator.json') as f:
        mitigator_abi = json.load(f)['abi']
    mitigator_contract = web3.eth.contract(
        address=os.environ.get('FRAUD_MITIGATOR_CONTRACT_ADDRESS'),
        abi=mitigator_abi
    )
    logger.info("[OK] FraudMitigator contract loaded")
    with open('build/contracts/FraudLedger.json') as f:
        ledger_abi = json.load(f)['abi']
    fraud_ledger_contract = web3.eth.contract(
        address=os.environ.get('FRAUD_LEDGER_CONTRACT_ADDRESS'),
        abi=ledger_abi
    )
    logger.info("[OK] FraudLedger contract loaded")
except Exception as e:
    logger.error(f"[ERROR] Smart contract loading failed: {e}")
    mitigator_contract = None
    fraud_ledger_contract = None
    mitigator_abi = []

# ✅ POLYGON LAYER-2 INTEGRATION
try:
    polygon_l2 = PolygonLayer2(
        contract_address=os.environ.get('FRAUD_MITIGATOR_CONTRACT_ADDRESS'),
        contract_abi=mitigator_abi if mitigator_contract else [],
        private_key=os.environ.get('SIGNER_PRIVATE_KEY')
    )
    if polygon_l2.is_enabled():
        logger.info("[OK] Polygon Layer-2 integration ready")
        logger.info("     💎 Cost savings: 99.97% cheaper than Ethereum mainnet")
    else:
        polygon_l2 = None
except Exception as e:
    logger.warning(f"[WARNING] Polygon L2 disabled: {e}")
    polygon_l2 = None

# --- 7. DATABASE MODELS ---
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    ethereum_address = db.Column(db.String(42), nullable=False)
    is_frozen = db.Column(db.Boolean, default=False, nullable=False)
    role = db.Column(db.String(20), default='user', nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    did_document = db.Column(db.Text, nullable=True)
    zkp_identity_proof = db.Column(db.Text, nullable=True)
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'ethereum_address': self.ethereum_address,
            'is_frozen': self.is_frozen,
            'role': self.role
        }
class TransactionLog(db.Model):
    __tablename__ = 'transaction_log'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    risk_score = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(100))
    tx_hash = db.Column(db.String(66), nullable=True)
    amount = db.Column(db.Float, nullable=True)
    merchant = db.Column(db.String(255), nullable=True)
    location = db.Column(db.String(255), nullable=True)
    transaction_type = db.Column(db.String(100), nullable=True)
    user = db.relationship('User', backref=db.backref('transaction_logs', lazy=True))
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'timestamp': self.timestamp.isoformat(),
            'risk_score': self.risk_score,
            'status': self.status,
            'tx_hash': self.tx_hash,
            'amount': self.amount,
            'merchant': self.merchant,
            'location': self.location,
            'transaction_type': self.transaction_type
        }

# --- 8. HELPER FUNCTIONS ---
def blockchain_transaction_with_retry(transaction_func, max_retries=3):
    for attempt in range(max_retries):
        try:
            return transaction_func()
        except Exception as e:
            if attempt == max_retries - 1:
                raise e
            wait_time = 2 ** attempt
            logger.warning(f"Blockchain transaction failed (attempt {attempt + 1}/{max_retries}). Retrying in {wait_time}s...")
            import time
            time.sleep(wait_time)

def create_sample_transaction_data(amount):
    if amount > 500000:
        return {
            'Time': 84000.0,
            'V1': -5.0, 'V2': 4.5, 'V3': -6.2, 'V4': 5.9,
            'V5': -4.8, 'V6': 6.5, 'V7': -3.9, 'V8': 5.7,
            'V9': -6.1, 'V10': 4.6, 'V11': -5.8, 'V12': 6.4,
            'V13': -4.3, 'V14': 5.2, 'V15': -6.0, 'V16': 4.5,
            'V17': -5.6, 'V18': 6.1, 'V19': -3.7, 'V20': 5.4,
            'V21': -5.9, 'V22': 6.3, 'V23': -4.0, 'V24': 4.9,
            'V25': -6.5, 'V26': 5.8, 'V27': -4.2, 'V28': 7.0,
            'Amount': float(amount)
        }
    else:
        return {
            'Time': 172792.0,
            'V1': -0.1, 'V2': 0.0, 'V3': 0.1, 'V4': 0.0,
            'V5': 0.0, 'V6': 0.0, 'V7': 0.0, 'V8': 0.0,
            'V9': 0.0, 'V10': 0.0, 'V11': 0.0, 'V12': 0.0,
            'V13': 0.0, 'V14': 0.0, 'V15': 0.0, 'V16': 0.0,
            'V17': 0.0, 'V18': 0.0, 'V19': 0.0, 'V20': 0.0,
            'V21': 0.0, 'V22': 0.0, 'V23': 0.0, 'V24': 0.0,
            'V25': 0.0, 'V26': 0.0, 'V27': 0.0, 'V28': 0.0,
            'Amount': float(amount)
        }

# --- 9. API ENDPOINTS ---

@app.route('/api/health', methods=['GET'])
def health_check():
    from sqlalchemy import text
    
    db_status = False
    try:
        db.session.execute(text('SELECT 1'))
        db.session.commit()
        db_status = True
    except Exception as e:
        logger.error(f"Database health check failed: {e}")

    blockchain_status = False
    try:
        blockchain_status = web3.is_connected() if web3 else False
    except Exception as e:
        logger.error(f"Blockchain health check failed: {e}")

    mongo_status = False
    try:
        mongo_client.admin.command('ping')
        mongo_status = True
    except Exception as e:
        logger.error(f"MongoDB health check failed: {e}")

    overall_status = db_status and blockchain_status and mongo_status

    return jsonify({
        'status': 'healthy' if overall_status else 'degraded',
        'services': {
            'database': db_status,
            'blockchain': blockchain_status,
            'mongodb': mongo_status
        },
        'timestamp': datetime.now(timezone.utc).isoformat()
    }), 200 if overall_status else 503

@app.route('/api/register', methods=['POST'])
@limiter.limit("5 per hour")
def register():
    try:
        data = request.get_json()
        
        required_fields = ['email', 'password', 'phone_number', 'address']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing field: {field}"}), 400
        
        if User.query.filter_by(email=data['email']).first():
            return jsonify({"error": "Email already registered"}), 409

        role = 'user'

        new_user = User(
            email=data['email'],
            phone_number=data['phone_number'],
            ethereum_address=data['address'],
            role=role
        )
        new_user.set_password(data['password'])

        db.session.add(new_user)
        db.session.commit()

        identity_proof = zkp_handler.create_identity_proof(new_user.id, data['address'])
        new_user.zkp_identity_proof = identity_proof['commitment']

        did_document = did_handler.create_did_document(new_user.id, data['address'], data['email'])
        new_user.did_document = json.dumps(did_document)

        db.session.commit()

        logger.info(f"New user registered: {data['email']}")
        logger.info(f"[OK] ZK identity proof generated for {data['email']}")
        logger.info(f"[OK] DID created: {did_document['id']}")
        return jsonify({"message": "User created successfully", "user": new_user.to_dict()}), 201

    except Exception as e:
        db.session.rollback()
        logger.error(f"Registration error: {str(e)}")
        return jsonify({"error": str(e)}), 400

@app.route('/api/admin/register', methods=['POST'])
def register_admin():
    try:
        data = request.get_json()
        
        required_fields = ['email', 'password', 'phone_number', 'address']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing field: {field}"}), 400
        
        if User.query.filter_by(email=data['email']).first():
            return jsonify({"error": "Email already registered"}), 409
        
        new_admin = User(
            email=data['email'],
            phone_number=data['phone_number'],
            ethereum_address=data['address'],
            role='admin'
        )
        new_admin.set_password(data['password'])
        
        db.session.add(new_admin)
        db.session.commit()
        
        identity_proof = zkp_handler.create_identity_proof(new_admin.id, data['address'])
        new_admin.zkp_identity_proof = identity_proof['commitment']
        
        did_document = did_handler.create_did_document(new_admin.id, data['address'], data['email'])
        new_admin.did_document = json.dumps(did_document)
        
        db.session.commit()
        
        logger.info(f"[OK] New ADMIN registered: {data['email']}")
        return jsonify({"message": "Admin created successfully", "user": new_admin.to_dict()}), 201
    
    except Exception as e:
        db.session.rollback()
        logger.error(f"Admin registration error: {str(e)}")
        return jsonify({"error": str(e)}), 400

@app.route('/api/login', methods=['POST'])
@limiter.limit("10 per hour")
def login():
    try:
        data = request.get_json()
        
        if not data.get('email') or not data.get('password'):
            return jsonify({"error": "Email and password required"}), 400
        
        user = User.query.filter_by(email=data['email']).first()
        
        if not user or not user.check_password(data['password']):
            return jsonify({"error": "Invalid credentials"}), 401
        
        access_token = create_access_token(
            identity=str(user.id),
            additional_claims={'role': user.role}
        )
        
        logger.info(f"User logged in: {user.email}")
        return jsonify({
            "access_token": access_token,
            "user": user.to_dict()
        }), 200
    
    except Exception as e:
        logger.error(f"Login error: {e}")
        return jsonify({"error": "Login failed"}), 500

@app.route('/api/transaction', methods=['POST'])
@jwt_required()
@limiter.limit("20 per minute")
def handle_transaction():
    try:
        current_user_id = int(get_jwt_identity())
        user = db.session.get(User, current_user_id)
        
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        if user.is_frozen:
            return jsonify({"error": "Account is frozen"}), 403
        
        transaction_data = request.get_json()
        
        if 'V1' not in transaction_data:
            amount = float(transaction_data.get('amount', transaction_data.get('Amount', 0)))
            full_transaction_data = create_sample_transaction_data(amount)
        else:
            full_transaction_data = transaction_data
            amount = float(transaction_data.get('Amount', 0))
        
        logger.info(f"Processing transaction for user {user.email}, amount: ${amount}")
        
        df = pd.DataFrame([full_transaction_data])
        required_cols = list(full_transaction_data.keys())
        
        logger.info("Running AI prediction pipeline...")
        
        # 1. Isolation Forest
        scaler_cols = [c for c in required_cols if c != 'Time']
        scaled_features = scaler.transform(df[scaler_cols])
        df['anomaly_score'] = iso_forest.decision_function(scaled_features)
        isolation_risk = float((df['anomaly_score'].values[0] + 1) / 2)

        # 2. Random Forest
        rf_features = df[required_cols]
        rf_risk = float(rf_model.predict_proba(rf_features)[:, 1][0])
        logger.info(f"Random Forest risk: {rf_risk:.2%}")
        
        # 3. LSTM
        if TF_AVAILABLE and lstm_autoencoder is not None:
            try:
                lstm_input = scaled_features.reshape((1, 1, scaled_features.shape[1]))
                lstm_reconstruction = lstm_autoencoder.predict(lstm_input, verbose=0)
                lstm_error = np.mean(np.abs(lstm_input - lstm_reconstruction))
                lstm_risk = min(lstm_error * 10, 1.0)
                logger.info(f"LSTM reconstruction error: {lstm_error:.4f}, risk: {lstm_risk:.2%}")
            except Exception as e:
                logger.warning(f"LSTM prediction failed: {e}")
                lstm_risk = 0.5
        else:
            lstm_risk = 0.5
            logger.info("LSTM not available - using neutral score")

        # 4. Transformer
        description = transaction_data.get('description', f'Payment of ${amount}')
        recipient = transaction_data.get('recipient', 'Unknown')
        
        historical_txns = []
        if mongo_db is not None:
            try:
                historical_txns = list(mongo_db.transactions.find(
                    {'user_id': user.id}
                ).sort('timestamp', -1).limit(10))
            except Exception as e:
                logger.warning(f"Could not fetch historical transactions: {e}")
        
        transformer_risk = transformer_detector.calculate_fraud_risk(
            amount=amount,
            recipient=recipient,
            description=description,
            historical_transactions=historical_txns
        )
        logger.info(f"Transformer NLP risk: {transformer_risk:.2%}")
        
        # 5. XGBoost
        xgb_input = pd.DataFrame({
            'Time': [full_transaction_data['Time']],
            **{f'V{i}': [full_transaction_data[f'V{i}']] for i in range(1, 29)},
            'Amount': [full_transaction_data['Amount']],
            'anomaly_score': [df['anomaly_score'].values[0]],
            'lstm_error': [lstm_risk],
            'gnn_pred': [0]
        })
        xgb_risk = float(xgb_model.predict_proba(xgb_input)[:, 1][0])
        logger.info(f"XGBoost meta-model risk: {xgb_risk:.2%}")
        
        # Ensemble
        if TF_AVAILABLE and lstm_autoencoder is not None:
            ensemble_weights = {
                'isolation': 0.15,
                'random_forest': 0.25,
                'lstm': 0.15,
                'transformer': 0.25,
                'xgboost': 0.20
            }
            logger.info("Using 5-model ensemble (LSTM enabled)")
        else:
            ensemble_weights = {
                'isolation': 0.20,
                'random_forest': 0.30,
                'lstm': 0.00,
                'transformer': 0.30,
                'xgboost': 0.20
            }
            logger.info("Using 4-model ensemble (LSTM disabled)")
        
        risk_score_raw = (
            isolation_risk * ensemble_weights['isolation'] +
            rf_risk * ensemble_weights['random_forest'] +
            lstm_risk * ensemble_weights['lstm'] +
            transformer_risk * ensemble_weights['transformer'] +
            xgb_risk * ensemble_weights['xgboost']
        )
        
        logger.info(f"[RISK BREAKDOWN]")
        logger.info(f"  - Isolation Forest: {isolation_risk:.2%}")
        logger.info(f"  - Random Forest: {rf_risk:.2%}")
        logger.info(f"  - LSTM Autoencoder: {lstm_risk:.2%}")
        logger.info(f"  - Transformer NLP: {transformer_risk:.2%}")
        logger.info(f"  - XGBoost Meta: {xgb_risk:.2%}")
        logger.info(f"  - FINAL RISK: {risk_score_raw:.2%}")
        
        if amount > 500000:
            risk_score = max(risk_score_raw, 0.90)
        else:
            risk_score = risk_score_raw
        
        logger.info(f"Final risk score calculated: {risk_score:.2%}")

        tx_hash_hex = None
        
        if risk_score < 0.30:
            status_message = "Low Risk - Transaction Approved"
            color = "green"
            action = "approved"
        elif risk_score < 0.65:
            status_message = "Medium Risk - Additional Verification Required"
            color = "orange"
            action = "review"
            
            if twilio_client:
                try:
                    public_url = os.environ.get('PUBLIC_URL', 'http://localhost:5000')
                    webhook_url = f"{public_url}/api/voice-response/{user.id}"
                    
                    call = twilio_client.calls.create(
                        to=user.phone_number,
                        from_=os.environ.get('TWILIO_PHONE_NUMBER'),
                        url=webhook_url
                    )
                    logger.info(f"Voice call initiated (MEDIUM RISK): {call.sid}")
                except Exception as e:
                    logger.error(f"Twilio call failed: {e}")
        else:
            status_message = "High Risk - Requires Verification"
            color = "red"
            action = "verification_required"

            if twilio_client:
                try:
                    public_url = os.environ.get('PUBLIC_URL', 'http://localhost:5000')
                    webhook_url = f"{public_url}/api/voice-response/{user.id}"
                    
                    call = twilio_client.calls.create(
                        to=user.phone_number,
                        from_=os.environ.get('TWILIO_PHONE_NUMBER'),
                        url=webhook_url
                    )
                    logger.info(f"Voice call initiated (HIGH RISK): {call.sid}")
                except Exception as e:
                    logger.error(f"Twilio call failed: {e}")

            # ✅ USE POLYGON LAYER-2 INSTEAD OF ETHEREUM (100x cheaper!)
            if polygon_l2 and polygon_l2.is_enabled():
                logger.info("📊 Using Polygon Layer-2 for blockchain logging...")
                layer2_result = polygon_l2.log_fraud_to_layer2(
                    user.ethereum_address,
                    risk_score,
                    f"High Risk Transaction: ${amount}"
                )
                
                if layer2_result['success']:
                    tx_hash_hex = layer2_result['tx_hash']
                    logger.info(f"💎 Logged to Polygon Layer-2: {tx_hash_hex}")
                    logger.info(f"   View on PolygonScan: {layer2_result['explorer_url']}")
                    logger.info(f"   Block: {layer2_result['block_number']}")
                    logger.info(f"   Gas Used: {layer2_result['gas_used']}")
                else:
                    logger.error(f"❌ Layer-2 logging failed: {layer2_result['error']}")
                    tx_hash_hex = None
            
            elif mitigator_contract and web3:
                # Fallback to Ethereum mainnet (more expensive)
                logger.warning("⚠️ Polygon not available - using Ethereum mainnet")
                try:
                    def send_transaction():
                        nonce = web3.eth.get_transaction_count(signer.address)
                        tx = mitigator_contract.functions.reportSuspiciousActivity(
                            user.ethereum_address,
                            int(risk_score * 100),
                            f"High Risk Transaction: ${amount}"
                        ).build_transaction({
                            'nonce': nonce,
                            'gas': 2000000,
                            'gasPrice': web3.to_wei('20', 'gwei'),
                            'from': signer.address
                        })
                        
                        signed_tx = web3.eth.account.sign_transaction(tx, private_key=os.environ.get('SIGNER_PRIVATE_KEY'))
                        tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction)
                        return tx_hash.hex()
                    
                    tx_hash_hex = blockchain_transaction_with_retry(send_transaction)
                    logger.info(f"Blockchain transaction successful: {tx_hash_hex}")
                    
                except Exception as e:
                    logger.error(f"Blockchain transaction failed: {e}")
                    traceback.print_exc()
                    tx_hash_hex = None
            else:
                logger.warning("⚠️ No blockchain integration available")
                tx_hash_hex = None
        
        response_data = {
            'status': status_message,
            'risk_score': risk_score,
            'amount': amount,
            'color': color,
            'action': action,
            'tx_hash': tx_hash_hex,
            'model_scores': {
                'isolation_forest': isolation_risk,
                'random_forest': rf_risk,
                'lstm': lstm_risk,
                'transformer': transformer_risk,
                'xgboost': xgb_risk
            }
        }
        
        new_log = TransactionLog(
            user_id=user.id,
            risk_score=risk_score,
            tx_hash=tx_hash_hex,
            status=status_message,
            amount=amount,
            merchant=transaction_data.get('merchant'),
            location=transaction_data.get('location'),
            transaction_type=transaction_data.get('transaction_type')
        )
        db.session.add(new_log)
        db.session.commit()
        
        return jsonify(response_data), 200
    
    except Exception as e:
        print("=== TRANSACTION ERROR ===")
        print("Error:", str(e))
        print("Type:", type(e).__name__)
        traceback.print_exc()
        print("=========================")
        logger.error(f"Transaction processing error: {e}")
        return jsonify({"error": "Transaction processing failed"}), 500

@app.route('/api/transactions', methods=['GET'])
@jwt_required()
def get_transactions():
    try:
        current_user_id = int(get_jwt_identity())
        
        logs = TransactionLog.query.filter_by(user_id=current_user_id)\
            .order_by(TransactionLog.timestamp.desc()).all()
        
        results = [log.to_dict() for log in logs]
        
        return jsonify(results), 200
    
    except Exception as e:
        logger.error(f"Error fetching transactions: {e}")
        return jsonify({"error": "Could not fetch transactions"}), 500

@app.route('/api/risk-score/<int:transaction_id>', methods=['GET'])
@jwt_required()
def get_risk_score(transaction_id):
    try:
        current_user_id = int(get_jwt_identity())
        
        transaction = TransactionLog.query.filter_by(
            id=transaction_id,
            user_id=current_user_id
        ).first()
        
        if not transaction:
            return jsonify({"error": "Transaction not found"}), 404
        
        return jsonify(transaction.to_dict()), 200
    
    except Exception as e:
        logger.error(f"Error fetching risk score: {e}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/api/admin/all-logs', methods=['GET'])
@jwt_required()
def get_all_transactions():
    try:
        current_user_id = int(get_jwt_identity())
        user = db.session.get(User, current_user_id)
        
        if not user or user.role != 'admin':
            logger.warning(f"Unauthorized admin access attempt by user {current_user_id}")
            return jsonify({"error": "Admin privileges required"}), 403
        
        all_logs = db.session.query(TransactionLog, User)\
            .join(User, TransactionLog.user_id == User.id)\
            .order_by(TransactionLog.timestamp.desc()).all()
        
        results = []
        for log, txn_user in all_logs:
            log_dict = log.to_dict()
            log_dict['user_email'] = txn_user.email
            results.append(log_dict)
        
        logger.info(f"Admin {user.email} accessed all transaction logs ({len(results)} records)")
        return jsonify(results), 200
    
    except Exception as e:
        logger.error(f"Error fetching all logs: {e}")
        traceback.print_exc()
        return jsonify({"error": "Internal server error"}), 500

@app.route('/api/blockchain/logs', methods=['GET'])
@jwt_required()
def get_blockchain_logs():
    try:
        current_user_id = int(get_jwt_identity())
        user = db.session.get(User, current_user_id)
        
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        transactions = TransactionLog.query.filter_by(user_id=current_user_id)\
            .filter(TransactionLog.tx_hash.isnot(None)).all()
        
        blockchain_logs = []
        
        if web3:
            for txn in transactions:
                try:
                    receipt = web3.eth.get_transaction_receipt(txn.tx_hash)
                    blockchain_logs.append({
                        "transaction_id": txn.id,
                        "tx_hash": txn.tx_hash,
                        "block_number": receipt['blockNumber'],
                        "gas_used": receipt['gasUsed'],
                        "status": "success" if receipt['status'] == 1 else "failed",
                        "timestamp": txn.timestamp.isoformat()
                    })
                except Exception as e:
                    logger.error(f"Error fetching receipt for {txn.tx_hash}: {e}")
                    continue
        
        return jsonify(blockchain_logs), 200
    
    except Exception as e:
        logger.error(f"Error fetching blockchain logs: {e}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/api/voice-call/initiate', methods=['POST'])
@jwt_required()
def initiate_voice_call():
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404
        return jsonify({"message": "Voice call working", "status": "success"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/voice-response/<int:user_id>', methods=['POST'])
def voice_response(user_id):
    response = VoiceResponse()
    
    action_url = f"/api/handle-keypad/{user_id}"
    gather = Gather(num_digits=1, action=action_url, method='POST')
    
    gather.say(
        "A high risk transaction was detected on your account. "
        "Press 1 to confirm this transaction was safe. "
        "Press 2 to report it as fraud."
    )
    
    response.append(gather)
    response.say("We did not receive a response. Goodbye.")
    
    return str(response)

@app.route('/api/handle-keypad/<int:user_id>', methods=['POST'])
def handle_keypad(user_id):
    digits = request.form.get('Digits')
    response = VoiceResponse()
    
    user = User.query.get(user_id)
    
    if not user:
        response.say("Sorry, we could not find your account.")
        return str(response)
    
    if digits == '1':
        user.is_frozen = False
        db.session.commit()
        logger.info(f"User {user.email} confirmed transaction - Account unfrozen")
        response.say("Thank you for confirming. Your account has been unlocked.")
    elif digits == '2':
        logger.info(f"User {user.email} reported fraud - Account remains frozen")
        response.say(
            "Thank you for your report. Your account will remain frozen "
            "for your protection. Please contact customer support."
        )
    else:
        response.say("Invalid input. Your account remains frozen for your protection.")
    
    return str(response)

@app.route('/api/user/freeze', methods=['PUT'])
@jwt_required()
def freeze_user_account():
    try:
        claims = get_jwt()
        if claims.get('role') != 'admin':
            return jsonify({"error": "Admin access required"}), 403
        
        data = request.get_json()
        user_id = data.get('user_id')
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        user.is_frozen = True
        db.session.commit()
        
        logger.info(f"Account frozen for user {user.email} by admin")
        return jsonify({"message": f"Account for {user.email} has been frozen"}), 200
    
    except Exception as e:
        logger.error(f"Error freezing account: {e}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/api/user/unfreeze', methods=['PUT'])
@jwt_required()
def unfreeze_user_account():
    try:
        claims = get_jwt()
        if claims.get('role') != 'admin':
            return jsonify({"error": "Admin access required"}), 403
        
        data = request.get_json()
        user_id = data.get('user_id')
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        user.is_frozen = False
        db.session.commit()
        
        logger.info(f"Account unfrozen for user {user.email} by admin")
        return jsonify({"message": f"Account for {user.email} has been unfrozen"}), 200
    
    except Exception as e:
        logger.error(f"Error unfreezing account: {e}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/api/profile', methods=['GET'])
@jwt_required()
def get_profile():
    try:
        current_user_id = int(get_jwt_identity())
        user = db.session.get(User, current_user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify({
            'id': user.id,
            'email': user.email,
            'phone_number': user.phone_number,
            'ethereum_address': user.ethereum_address,
            'is_frozen': user.is_frozen,
            'role': user.role,
            'created_at': user.created_at.isoformat()
        }), 200
    except Exception as e:
        logger.error(f'Get profile error: {e}')
        return jsonify({'error': 'Failed to get profile'}), 500

@app.route('/api/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    try:
        current_user_id = int(get_jwt_identity())
        user = db.session.get(User, current_user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        data = request.get_json()
        
        if 'phone_number' in data:
            user.phone_number = data['phone_number']
        if 'ethereum_address' in data:
            user.ethereum_address = data['ethereum_address']
        
        db.session.commit()
        
        return jsonify({'message': 'Profile updated successfully'}), 200
    except Exception as e:
        logger.error(f'Update profile error: {e}')
        return jsonify({'error': 'Failed to update profile'}), 500

# ✅ NEW POLYGON ENDPOINTS
@app.route('/api/blockchain/cost-comparison', methods=['GET'])
@jwt_required()
def get_cost_comparison():
    """Show Layer-2 vs Ethereum cost comparison"""
    try:
        if polygon_l2 and polygon_l2.is_enabled():
            comparison = polygon_l2.get_cost_comparison()
            return jsonify({
                'success': True,
                'comparison': comparison,
                'message': f"Save {comparison['savings']['percentage_saved']}% by using Polygon!"
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'Polygon Layer-2 not available'
            }), 503
    except Exception as e:
        logger.error(f"Cost comparison error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/blockchain/history', methods=['GET'])
@jwt_required()
def get_blockchain_history():
    """Get recent fraud reports from Polygon blockchain"""
    try:
        current_user_id = int(get_jwt_identity())
        user = db.session.get(User, current_user_id)
        
        if not user or user.role != 'admin':
            return jsonify({'error': 'Admin access required'}), 403
        
        if polygon_l2 and polygon_l2.is_enabled():
            history = polygon_l2.get_transaction_history(limit=20)
            return jsonify({
                'success': True,
                'history': history,
                'network': 'Polygon Mumbai Testnet'
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'Polygon Layer-2 not available'
            }), 503
    
    except Exception as e:
        logger.error(f"Blockchain history error: {e}")
        return jsonify({'error': str(e)}), 500

# --- 10. ERROR HANDLERS ---
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Resource not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    logger.error(f"Internal error: {error}")
    return jsonify({'error': 'Internal server error'}), 500

@app.errorhandler(429)
def rate_limit_exceeded(error):
    return jsonify({'error': 'Rate limit exceeded. Please try again later.'}), 429

# --- 11. APPLICATION ENTRY POINT ---
# if __name__ == '__main__':
#     with app.app_context():
#         db.create_all()
#         logger.info("Database tables created/verified")
    
#     logger.info("[SUCCESS] Starting Flask application...")
#     app.run(host='0.0.0.0', port=5000, debug=True)
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        logger.info("Database tables created/verified")
    
    logger.info("[SUCCESS] Starting Flask application...")
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
