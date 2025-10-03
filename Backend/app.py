# app.py (Final Version with All Fixes & Correct Filenames)

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
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
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

app.config.from_mapping(
    SECRET_KEY = os.environ.get('SECRET_KEY'),
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY'),
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL'),
    SQLALCHEMY_TRACK_MODIFICATIONS = False,
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
)
db = SQLAlchemy(app)
jwt = JWTManager(app)

# --- 2. SERVICE CONNECTIONS ---
mongo_client = MongoClient(os.environ.get('MONGO_URI'))
mongo_db = mongo_client.get_database('fraud_logs_db')
web3 = Web3(Web3.HTTPProvider(os.environ.get('INFURA_URL', 'http://127.0.0.1:7545')))
signer = web3.eth.account.from_key(os.environ.get('SIGNER_PRIVATE_KEY'))
web3.eth.default_account = signer.address
twilio_client = TwilioClient(os.environ.get('TWILIO_ACCOUNT_SID'), os.environ.get('TWILIO_AUTH_TOKEN'))

# --- 3. AI MODEL AND CONTRACT LOADING (CORRECTED) ---
print("Loading AI models and contracts...")
try:
    model_path = 'models/trained_models/'
    
    # --- FILENAME FIXES TO MATCH YOUR SCREENSHOT ---
    iso_forest = joblib.load(os.path.join(model_path, 'isolation_forest.joblib'))
    
    lstm_autoencoder = tf.keras.models.load_model(
        os.path.join(model_path, 'lstm_autoencoder.h5'),
        custom_objects={'mae': tf.keras.losses.MeanAbsoluteError()}
    )
    
    xgb_model = xgb.XGBClassifier()
    xgb_model.load_model(os.path.join(model_path, 'xgb_risk_model.json')) # Correct loading method
    
    # This file is critical and is created by the corrected training script
    scaler = joblib.load(os.path.join(model_path, 'scaler.joblib'))
    # --- END OF FILENAME FIXES ---

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
    def set_password(self, password): self.password_hash = generate_password_hash(password)
    def check_password(self, password): return check_password_hash(self.password_hash, password)

class TransactionLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    risk_score = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(100))
    tx_hash = db.Column(db.String(66), nullable=True)

# --- 5. API ENDPOINTS ---
@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    if User.query.filter_by(email=data['email']).first():
        return jsonify({"message": "Email already exists"}), 409
    new_user = User(
        email=data['email'],
        phone_number=data['phone_number'],
        ethereum_address=data['address']
    )
    new_user.set_password(data['password'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User created successfully"}), 201

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    if not user or not user.check_password(data['password']):
        return jsonify({"message": "Invalid credentials"}), 401
    
    # --- JWT FIX: Use a simple user ID for the token identity ---
    access_token = create_access_token(identity=user.id)
    return jsonify(access_token=access_token)

@app.route('/api/transaction', methods=['POST'])
@jwt_required()
def handle_transaction():
    try:
        # --- JWT FIX: Get the user ID from the token and query the database ---
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        if user.is_frozen:
            return jsonify(error="Account is frozen"), 403

        transaction_data = request.get_json()
        df = pd.DataFrame([transaction_data])
        
        required_cols = ['Time', 'V1', 'V2', 'V3', 'V4', 'V5', 'V6', 'V7', 'V8', 'V9', 'V10', 'V11', 'V12', 'V13', 'V14', 'V15', 'V16', 'V17', 'V18', 'V19', 'V20', 'V21', 'V22', 'V23', 'V24', 'V25', 'V26', 'V27', 'V28', 'Amount']
        if not all(col in df.columns for col in required_cols):
            return jsonify({"error": "Missing required transaction features"}), 422
        
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
                twilio_client.calls.create(to=user.phone_number, from_=os.environ.get('TWILIO_PHONE_NUMBER'), url=f"{os.environ.get('PUBLIC_URL')}/api/voice-response")
                print(f"Initiated voice call to {user.phone_number}")
            except Exception as e:
                print(f"Twilio call failed: {e}")

            nonce = web3.eth.get_transaction_count(signer.address)
            tx = mitigator_contract.functions.reportSuspiciousActivity(user.ethereum_address, int(risk_score * 100), "High Risk Transaction").build_transaction({'nonce': nonce, 'gas': 2000000, 'gasPrice': web3.to_wei('20', 'gwei')})
            signed_tx = web3.eth.account.sign_transaction(tx, private_key=os.environ.get('SIGNER_PRIVATE_KEY'))
            tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
            tx_hash_hex = tx_hash.hex()
            print(f"Blockchain transaction submitted: {tx_hash_hex}")
            response_data.update({'status': status_message, 'tx_hash': tx_hash_hex})

        elif risk_score > 0.5:
            status_message = "Medium Risk: Manual Review Required"
            response_data.update({'status': status_message})

        new_log = TransactionLog(user_id=user.id, risk_score=float(risk_score), tx_hash=tx_hash_hex, status=status_message)
        db.session.add(new_log)
        db.session.commit()
        
        mongo_db.transaction_logs.insert_one({"user_id": user.id, "timestamp": datetime.utcnow(), "risk_score": float(risk_score), "status": status_message, "details": transaction_data})
        
        return jsonify(response_data)

    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": "An internal server error occurred"}), 500

@app.route('/api/voice-response', methods=['POST'])
def voice_response():
    response = VoiceResponse()
    gather = Gather(num_digits=1, action='/api/handle-keypad', method='POST')
    gather.say("A high risk transaction was detected. Press 1 to confirm it was you. Press 2 to report as fraud.")
    response.append(gather)
    response.say("We did not receive a response. Goodbye.")
    return str(response)

@app.route('/api/handle-keypad', methods=['POST'])
def handle_keypad():
    digits = request.form.get('Digits')
    if digits == '1':
        print("User authorized transaction via keypad.")
    elif digits == '2':
        print("User reported fraud via keypad.")
    response = VoiceResponse()
    response.say("Thank you for your response.")
    return str(response)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(port=5000, debug=True)