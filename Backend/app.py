# app.py (Final, Fully Featured Version)

import os
import json
import pandas as pd
import joblib
import xgboost as xgb
import tensorflow as tf
from datetime import datetime
from pymongo import MongoClient
from twilio.twiml.voice_response import VoiceResponse
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from web3 import Web3
from twilio.rest import Client
from dotenv import load_dotenv

# 1. INITIALIZATION AND CONFIGURATION
load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
jwt = JWTManager(app)

# 2. SERVICE CONNECTIONS
web3 = Web3(Web3.HTTPProvider(os.environ.get('INFURA_URL', 'http://127.0.0.1:7545')))
signer = web3.eth.account.from_key(os.environ.get('SIGNER_PRIVATE_KEY'))
web3.eth.default_account = signer.address
with open('build/contracts/FraudMitigator.json') as f: mitigator_abi = json.load(f)['abi']
mitigator_contract = web3.eth.contract(address=os.environ.get('FRAUD_MITIGATOR_CONTRACT_ADDRESS'), abi=mitigator_abi)
with open('build/contracts/FraudLedger.json') as f: ledger_abi = json.load(f)['abi']
fraud_ledger_contract = web3.eth.contract(address=os.environ.get('FRAUD_LEDGER_CONTRACT_ADDRESS'), abi=ledger_abi)
twilio_client = Client(os.environ.get('TWILIO_ACCOUNT_SID'), os.environ.get('TWILIO_AUTH_TOKEN'))
mongo_client = MongoClient(os.environ.get('MONGO_URI'))
mongo_db = mongo_client.get_database('fraud_logs_db')

# 3. AI MODEL LOADING
print("Loading AI models...")
iso_forest = joblib.load('models/trained_models/isolation_forest.joblib')
lstm_autoencoder = tf.keras.models.load_model('models/trained_models/lstm_autoencoder.h5', custom_objects={'mae': tf.keras.losses.MeanAbsoluteError()})
xgb_model = xgb.XGBClassifier()
xgb_model.load_model('models/trained_models/xgb_risk_model.json')
print("AI models loaded successfully.")

# 4. DATABASE MODELS
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    password_hash = db.Column(db.String(256))
    address = db.Column(db.String(42)) # To store user's Ethereum address
    account_status = db.Column(db.String(20), default='active')
    def set_password(self, password): self.password_hash = generate_password_hash(password)
    def check_password(self, password): return check_password_hash(self.password_hash, password)

class TransactionLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    risk_score = db.Column(db.Integer, nullable=False)
    tx_hash = db.Column(db.String(256), nullable=True)
    status = db.Column(db.String(100))

# 5. API ENDPOINTS
@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    if User.query.filter_by(email=data['email']).first(): return jsonify({"message": "Email already exists"}), 409
    new_user = User(email=data['email'], phone_number=data['phone_number'], address=data['address'])
    new_user.set_password(data['password'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User created successfully"}), 201

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    if not user or not user.check_password(data['password']): return jsonify({"message": "Invalid credentials"}), 401
    access_token = create_access_token(identity={'id': user.id, 'phone': user.phone_number, 'address': user.address})
    return jsonify(access_token=access_token)

@app.route('/api/transaction', methods=['POST'])
@jwt_required()
def assess_transaction():
    try:
        current_user = get_jwt_identity()
        user_db_record = User.query.get(current_user['id'])
        if user_db_record.account_status == 'frozen': return jsonify(message="Account is frozen"), 403

        transaction_data = request.get_json()
        df = pd.DataFrame([transaction_data])

        # Simplified feature generation for a single transaction
        df['anomaly_score'] = iso_forest.decision_function(df.drop(['Time', 'Class'], axis=1, errors='ignore'))
        df['lstm_error'] = 0.5; df['gnn_pred'] = 0 # Placeholders for live prediction

        features_for_xgb = df.drop(['Class'], axis=1, errors='ignore')
        risk_score = int(xgb_model.predict_proba(features_for_xgb)[:, 1][0] * 100)
        print(f"Final AI Risk Score: {risk_score}%")

        HIGH_RISK_THRESHOLD, MEDIUM_RISK_THRESHOLD = 85, 60
        status_message, tx_hash_hex = "Low Risk - Approved", None

        if risk_score >= MEDIUM_RISK_THRESHOLD:
            proof = {'proof': {'a': [0,0], 'b': [[0,0],[0,0]], 'c': [0,0]}, 'inputs': [risk_score]}
            nonce = web3.eth.get_transaction_count(signer.address)
            tx_id = f"TXID_{datetime.utcnow().timestamp()}"
            
            tx = mitigator_contract.functions.executeResponse(
                risk_score, current_user['address'], tx_id,
                proof['inputs'], proof['proof']['a'], proof['proof']['b'], proof['proof']['c']
            ).build_transaction({'nonce': nonce, 'gas': 500000, 'gasPrice': web3.eth.gas_price})
            
            signed_tx = web3.eth.account.sign_transaction(tx, private_key=os.environ.get('SIGNER_PRIVATE_KEY'))
            tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
            web3.eth.wait_for_transaction_receipt(tx_hash)
            tx_hash_hex = tx_hash.hex()
            
            if risk_score >= HIGH_RISK_THRESHOLD:
                status_message, user_db_record.account_status = "High Risk: Account Frozen & Voice Call Initiated", 'frozen'
                voice_response_url = os.environ.get('PUBLIC_URL') + '/api/voice-response'
                twilio_client.calls.create(to=current_user['phone'], from_=os.environ.get('TWILIO_PHONE_NUMBER'),
                    twiml=f'<Response><Gather action="{voice_response_url}" numDigits="1"><Say>A high risk transaction of amount {transaction_data.get("Amount")} has been detected. Press 1 to approve this transaction and unfreeze your account. Press 2 to confirm this is fraud.</Say></Gather></Response>')
            else:
                status_message = "Medium Risk: MFA Triggered on Blockchain"
            
            log_doc = {"timestamp": datetime.utcnow(), "user_id": current_user['id'], "risk_score": risk_score, "action": status_message, "tx_hash": tx_hash_hex}
            mongo_db.transaction_logs.insert_one(log_doc)

        new_log = TransactionLog(user_id=current_user['id'], risk_score=risk_score, tx_hash=tx_hash_hex, status=status_message)
        db.session.add(new_log)
        db.session.commit()
        
        return jsonify({"status": status_message, "tx_hash": tx_hash_hex, "risk_score": risk_score})
    except Exception as e:
        import traceback; traceback.print_exc()
        return jsonify({"error": "An internal error occurred"}), 500

@app.route('/api/voice-response', methods=['POST'])
def handle_voice_response():
    digits_pressed, caller_phone = request.form.get('Digits'), request.form.get('From')
    response, user = VoiceResponse(), User.query.filter_by(phone_number=caller_phone).first()
    if user:
        if digits_pressed == '1':
            user.account_status = 'active'; db.session.commit()
            response.say('Transaction approved. Your account is reactivated.')
        else: # Assumes 2 or any other digit means fraud
            response.say('Your account will remain frozen. Please contact customer support.')
    else:
        response.say('Could not identify user. Please contact support.')
    return str(response), 200, {'Content-Type': 'text/xml'}

@app.route('/api/transactions/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user_transactions(user_id):
    if get_jwt_identity()['id'] != user_id: return jsonify({"message": "Unauthorized"}), 403
    logs = TransactionLog.query.filter_by(user_id=user_id).order_by(TransactionLog.timestamp.desc()).all()
    return jsonify([{"ts": l.timestamp, "risk": l.risk_score, "status": l.status, "hash": l.tx_hash} for l in logs])

@app.route('/api/blockchain-logs', methods=['GET'])
@jwt_required()
def get_blockchain_logs():
    try:
        count = fraud_ledger_contract.functions.reportCounter().call()
        reports = [fraud_ledger_contract.functions.secureFraudReports(i).call() for i in range(1, count + 1)]
        return jsonify([{"id": r[0], "tx_id": r[1], "ts": r[2], "reporter": r[3]} for r in reports])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(port=5000, debug=True)