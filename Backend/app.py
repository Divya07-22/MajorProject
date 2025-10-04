import os
import json
import pandas as pd
import joblib
import xgboost as xgb
import tensorflow as tf
from datetime import datetime, timedelta
from pymongo import MongoClient
from twilio.twiml.voice_response import VoiceResponse, Gather
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, get_jwt
from werkzeug.security import generate_password_hash, check_password_hash
from web3 import Web3
from twilio.rest import Client as TwilioClient
from dotenv import load_dotenv
from flask_cors import CORS
import numpy as np
import traceback

# --- 1. INITIALIZATION AND CONFIGURATION ---
load_dotenv()
app = Flask(__name__)
CORS(app)
app.config.from_mapping(SECRET_KEY = os.environ.get('SECRET_KEY'), JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY'), SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL'), SQLALCHEMY_TRACK_MODIFICATIONS = False, JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1))
db = SQLAlchemy(app)
jwt = JWTManager(app)

# --- 2. SERVICE CONNECTIONS ---
mongo_client = MongoClient(os.environ.get('MONGO_URI'))
mongo_db = mongo_client.get_database('fraud_logs_db')
web3 = Web3(Web3.HTTPProvider(os.environ.get('INFURA_URL', 'http://127.0.0.1:7545')))
signer = web3.eth.account.from_key(os.environ.get('SIGNER_PRIVATE_KEY'))
web3.eth.default_account = signer.address
twilio_client = TwilioClient(os.environ.get('TWILIO_ACCOUNT_SID'), os.environ.get('TWILIO_AUTH_TOKEN'))

# --- 3. AI MODEL AND CONTRACT LOADING ---
print("Loading AI models and contracts...")
try:
    model_path = 'models/trained_models/'
    iso_forest = joblib.load(os.path.join(model_path, 'isolation_forest.joblib'))
    lstm_autoencoder = tf.keras.models.load_model(os.path.join(model_path, 'lstm_autoencoder.h5'), custom_objects={'mae': tf.keras.losses.MeanAbsoluteError()})
    xgb_model = xgb.XGBClassifier()
    xgb_model.load_model(os.path.join(model_path, 'xgb_risk_model.json'))
    scaler = joblib.load(os.path.join(model_path, 'scaler.joblib'))
    with open('build/contracts/FraudMitigator.json') as f: mitigator_abi = json.load(f)['abi']
    mitigator_contract = web3.eth.contract(address=os.environ.get('FRAUD_MITIGATOR_CONTRACT_ADDRESS'), abi=mitigator_abi)
    with open('build/contracts/FraudLedger.json') as f: ledger_abi = json.load(f)['abi']
    fraud_ledger_contract = web3.eth.contract(address=os.environ.get('FRAUD_LEDGER_CONTRACT_ADDRESS'), abi=ledger_abi)
    print("AI models and contracts loaded successfully.")
except Exception as e:
    print(f"FATAL: Could not load models or contracts. Have you run the training scripts? Error: {e}")
    exit()

# --- 4. DATABASE MODELS ---
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    password_hash = db.Column(db.String(256))
    ethereum_address = db.Column(db.String(42), nullable=False)
    is_frozen = db.Column(db.Boolean, default=False, nullable=False)
    role = db.Column(db.String(20), default='user', nullable=False)
    def set_password(self, password): self.password_hash = generate_password_hash(password)
    def check_password(self, password): return check_password_hash(self.password_hash, password)

class TransactionLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    risk_score = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(100))
    tx_hash = db.Column(db.String(66), nullable=True)
    user = db.relationship('User', backref=db.backref('transaction_logs', lazy=True))


# --- 5. API ENDPOINTS ---
@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    if User.query.filter_by(email=data['email']).first(): return jsonify({"message": "Email already exists"}), 409
    role = 'admin' if data['email'] == 'admin@example.com' else 'user'
    new_user = User(email=data['email'], phone_number=data['phone_number'], ethereum_address=data['address'], role=role)
    new_user.set_password(data['password'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User created successfully"}), 201


@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    if not user or not user.check_password(data['password']): return jsonify({"message": "Invalid credentials"}), 401
    
    # THIS IS THE CRITICAL FIX: The identity is a simple number.
    access_token = create_access_token(identity=user.id, additional_claims={'role': user.role})
    
    return jsonify(access_token=access_token)


@app.route('/api/transaction', methods=['POST'])
@jwt_required()
def handle_transaction():
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        if not user: return jsonify({"error": "User not found"}), 404
        if user.is_frozen: return jsonify(error="Account is frozen"), 403

        transaction_data = request.get_json()
        
        # This handles both full data from old tests and simple data from the frontend
        if 'V1' not in transaction_data:
            amount = float(transaction_data.get('amount', 0))
            full_transaction_data = {'Time': 172792.0, 'V1': -1.359807, 'V2': -0.072781, 'V3': 2.536347, 'V4': 1.378155, 'V5': -0.338321, 'V6': 0.462388, 'V7': 0.239599, 'V8': 0.098698, 'V9': 0.363787, 'V10': 0.090794, 'V11': -0.5516, 'V12': -0.617801, 'V13': -0.99139, 'V14': -0.311169, 'V15': 1.468177, 'V16': -0.470401, 'V17': 0.207971, 'V18': 0.025791, 'V19': 0.403993, 'V20': 0.251412, 'V21': -0.018307, 'V22': 0.277838, 'V23': -0.110474, 'V24': 0.066928, 'V25': 0.128539, 'V26': -0.189115, 'V27': 0.133558, 'V28': -0.021053, 'Amount': amount}
        else:
            full_transaction_data = transaction_data

        df = pd.DataFrame([full_transaction_data])
        required_cols = list(full_transaction_data.keys())
        
        print("Running full AI prediction pipeline...")
        scaled_features = scaler.transform(df[required_cols])
        df['anomaly_score'] = iso_forest.predict(scaled_features)
        reconstruction = lstm_autoencoder.predict(scaled_features)
        mse = np.mean(np.power(scaled_features - reconstruction, 2), axis=1)
        df['lstm_error'] = mse
        df['gnn_pred'] = 0
        features_for_xgb = df[required_cols + ['anomaly_score', 'lstm_error', 'gnn_pred']]
        risk_score = xgb_model.predict_proba(features_for_xgb)[:, 1][0]
        print(f"Final AI Risk Score: {risk_score:.2%}")

        status_message, tx_hash_hex = "Low Risk - Approved", None
        response_data = {'status': status_message, 'risk_score': float(risk_score)}

        if risk_score > 0.85:
            status_message = "High Risk: Account Frozen & Reported"
            user.is_frozen = True
            
            try:
                public_url = os.environ.get('PUBLIC_URL')
                webhook_url = f"{public_url}/api/voice-response/{user.id}"
                twilio_client.calls.create(to=user.phone_number, from_=os.environ.get('TWILIO_PHONE_NUMBER'), url=webhook_url)
            except Exception as e:
                print(f"Twilio call failed: {e}")

            nonce = web3.eth.get_transaction_count(signer.address)
            tx = mitigator_contract.functions.reportSuspiciousActivity(user.ethereum_address, int(risk_score * 100), "High Risk Transaction").build_transaction({'nonce': nonce, 'gas': 2000000, 'gasPrice': web3.to_wei('20', 'gwei')})
            signed_tx = web3.eth.account.sign_transaction(tx, private_key=os.environ.get('SIGNER_PRIVATE_KEY'))
            tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
            tx_hash_hex = tx_hash.hex()
            response_data.update({'status': status_message, 'tx_hash': tx_hash_hex})

        elif risk_score > 0.5:
            status_message = "Medium Risk: Manual Review Required"
            response_data.update({'status': status_message})

        new_log = TransactionLog(user_id=user.id, risk_score=float(risk_score), tx_hash=tx_hash_hex, status=status_message)
        db.session.add(new_log)
        db.session.commit()
        mongo_db.transaction_logs.insert_one({"user_id": user.id, "timestamp": datetime.utcnow(), "risk_score": float(risk_score), "status": status_message, "details": full_transaction_data})
        
        return jsonify(response_data)

    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": "An internal server error occurred"}), 500


@app.route('/api/transactions', methods=['GET'])
@jwt_required()
def get_transactions():
    try:
        current_user_id = get_jwt_identity()
        logs = TransactionLog.query.filter_by(user_id=current_user_id).order_by(TransactionLog.timestamp.desc()).all()
        results = [{"id": log.id, "timestamp": log.timestamp.isoformat(), "risk_score": log.risk_score, "status": log.status, "tx_hash": log.tx_hash} for log in logs]
        return jsonify(results), 200
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": "An internal server error occurred"}), 500


@app.route('/api/admin/all-logs', methods=['GET'])
@jwt_required()
def get_all_transactions():
    claims = get_jwt()
    if claims.get('role') != 'admin':
        return jsonify({"msg": "Admins only!"}), 403
    all_logs = db.session.query(TransactionLog, User).join(User, TransactionLog.user_id == User.id).order_by(TransactionLog.timestamp.desc()).all()
    results = [{"id": log.id, "user_email": user.email, "timestamp": log.timestamp.isoformat(), "risk_score": log.risk_score, "status": log.status, "tx_hash": log.tx_hash} for log, user in all_logs]
    return jsonify(results), 200


@app.route('/api/voice-response/<int:user_id>', methods=['POST'])
def voice_response(user_id):
    response = VoiceResponse()
    action_url = f"/api/handle-keypad/{user_id}"
    gather = Gather(num_digits=1, action=action_url, method='POST')
    gather.say("A high risk transaction was detected on your account. Press 1 to confirm this transaction was safe. Press 2 to report it as fraud.")
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
        print(f"User {user.email} confirmed transaction. Account unfrozen.")
        response.say("Thank you for confirming. Your account has been unlocked.")
    elif digits == '2':
        print(f"User {user.email} reported fraud. Account remains frozen.")
        response.say("Thank you for your report. Your account will remain frozen for your protection. Please contact customer support.")
    else:
        response.say("Invalid input. Your account remains frozen for your protection.")
    return str(response)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(port=5000, debug=True)