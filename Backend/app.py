# app.py
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
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, JWTManager
from werkzeug.security import generate_password_hash, check_password_hash
from web3 import Web3
from twilio.rest import Client as TwilioClient
from dotenv import load_dotenv

load_dotenv()

# --- Configurations ---
SECRET_KEY = os.getenv('SECRET_KEY')
JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
DATABASE_URL = os.getenv('DATABASE_URL')
MONGO_URI = os.getenv('MONGO_URI')
INFURA_URL = os.getenv('INFURA_URL')
SIGNER_PRIVATE_KEY = os.getenv('SIGNER_PRIVATE_KEY')
FRAUD_MITIGATOR_ADDRESS = os.getenv('FRAUD_MITIGATOR_CONTRACT_ADDRESS')
FRAUD_LEDGER_ADDRESS = os.getenv('FRAUD_LEDGER_CONTRACT_ADDRESS')
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_PHONE_NUMBER = os.getenv('TWILIO_PHONE_NUMBER')
PUBLIC_URL = os.getenv('PUBLIC_URL')

# --- Initialization ---
app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['JWT_SECRET_KEY'] = JWT_SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)

db = SQLAlchemy(app)
jwt = JWTManager(app)
mongo_client = MongoClient(MONGO_URI)
mongo_db = mongo_client.get_database()
web3 = Web3(Web3.HTTPProvider(INFURA_URL))
twilio_client = TwilioClient(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
signer_account = web3.eth.account.from_key(SIGNER_PRIVATE_KEY)

# --- Database Models ---
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    ethereum_address = db.Column(db.String(42), nullable=False)
    is_frozen = db.Column(db.Boolean, default=False, nullable=False)

class TransactionLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    risk_score = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(100), nullable=False)
    tx_hash = db.Column(db.String(66))

# --- Load AI Models ---
print("Loading AI models...")
try:
    model_path = 'models/trained_models/'
    iso_forest = joblib.load(os.path.join(model_path, 'isolation_forest_model.joblib'))
    lstm_autoencoder = tf.keras.models.load_model(os.path.join(model_path, 'lstm_autoencoder.h5'))
    xgb_model = joblib.load(os.path.join(model_path, 'final_risk_model.joblib'))
    scaler = joblib.load(os.path.join(model_path, 'scaler.joblib'))
    with open('build/contracts/FraudMitigator.json') as f:
        mitigator_abi = json.load(f)['abi']
    with open('build/contracts/FraudLedger.json') as f:
        ledger_abi = json.load(f)['abi']
    mitigator_contract = web3.eth.contract(address=FRAUD_MITIGATOR_ADDRESS, abi=mitigator_abi)
    ledger_contract = web3.eth.contract(address=FRAUD_LEDGER_ADDRESS, abi=ledger_abi)
    print("AI models and contracts loaded successfully.")
except Exception as e:
    print(f"FATAL: Could not load models or contracts. Error: {e}")
    exit()

# --- API Endpoints ---
@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    hashed_password = generate_password_hash(data['password'])
    new_user = User(
        email=data['email'],
        password_hash=hashed_password,
        phone_number=data['phone_number'],
        ethereum_address=data['address']
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully'}), 201

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    if user and check_password_hash(user.password_hash, data['password']):
        access_token = create_access_token(identity={'id': user.id, 'address': user.ethereum_address})
        return jsonify(access_token=access_token)
    return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/api/transaction', methods=['POST'])
@jwt_required()
def handle_transaction():
    current_user_identity = get_jwt_identity()
    user = User.query.get(current_user_identity['id'])

    if user.is_frozen:
        return jsonify({'error': 'Account is frozen due to suspicious activity'}), 403

    data = request.get_json()
    tx_df = pd.DataFrame([data])
    
    # --- THIS IS THE PART WITH THE BUG FIX ---
    # The list of required columns now correctly matches the creditcard.csv header
    required_cols = [
        'Time', 'V1', 'V2', 'V3', 'V4', 'V5', 'V6', 'V7', 'V8', 'V9', 'V10',
        'V11', 'V12', 'V13', 'V14', 'V15', 'V16', 'V17', 'V18', 'V19', 'V20',
        'V21', 'V22', 'V23', 'V24', 'V25', 'V26', 'V27', 'V28', 'Amount'
    ]

    if not all(col in tx_df.columns for col in required_cols):
        return jsonify({"error": "Missing required transaction features"}), 422

    # --- AI Prediction Pipeline ---
    scaled_features = scaler.transform(tx_df[required_cols])
    
    # 1. Anomaly Detection
    tx_df['anomaly_score'] = iso_forest.predict(scaled_features)
    print(f"Isolation Forest Score: {tx_df['anomaly_score'].iloc[0]}")

    # 2. Behavior Profiling (LSTM)
    reconstruction = lstm_autoencoder.predict(scaled_features)
    mse = tf.reduce_mean(tf.square(scaled_features - reconstruction), axis=1).numpy()
    tx_df['lstm_error'] = mse
    print(f"LSTM Reconstruction Error: {tx_df['lstm_error'].iloc[0]}")

    # 3. GNN Prediction (Placeholder for this example)
    tx_df['gnn_pred'] = 1 if tx_df['Amount'].iloc[0] > 1000 else 0 # Simple rule as a placeholder
    print(f"GNN Prediction: {tx_df['gnn_pred'].iloc[0]}")

    # 4. Final Risk Model (XGBoost)
    final_features = tx_df[required_cols + ['anomaly_score', 'lstm_error', 'gnn_pred']]
    risk_score = xgb_model.predict_proba(final_features)[:, 1][0]
    print(f"Final AI Risk Score: {risk_score:.2%}")

    # --- Decision Logic ---
    if risk_score > 0.85:
        # High risk: Freeze account and report
        user.is_frozen = True
        db.session.commit()
        status = "High Risk: Account Frozen & Reported to Blockchain"
        
        # Initiate Twilio call
        try:
            twilio_client.calls.create(
                to=user.phone_number,
                from_=TWILIO_PHONE_NUMBER,
                url=f"{PUBLIC_URL}/api/voice-response"
            )
            print(f"Initiated voice call to {user.phone_number}")
        except Exception as e:
            print(f"Error making Twilio call: {e}")

        # Send to Blockchain
        nonce = web3.eth.get_transaction_count(signer_account.address)
        tx = mitigator_contract.functions.reportSuspiciousActivity(
            user.ethereum_address, int(risk_score * 100), "High Risk Transaction"
        ).build_transaction({
            'chainId': 1337, 'gas': 2000000, 'gasPrice': web3.to_wei('20', 'gwei'), 'nonce': nonce
        })
        signed_tx = web3.eth.account.sign_transaction(tx, private_key=SIGNER_PRIVATE_KEY)
        tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        print(f"Submitting transaction to smart contract... Hash: {tx_hash.hex()}")
        
        response_data = {'status': status, 'tx_hash': tx_hash.hex()}
        
    elif risk_score > 0.5:
        status = "Medium Risk: Manual Review Required"
        response_data = {'status': status}
    else:
        status = "Low Risk: Transaction Approved"
        response_data = {'status': status}
        
    # Log to both databases
    log_entry = TransactionLog(user_id=user.id, risk_score=risk_score, status=status, tx_hash=response_data.get('tx_hash'))
    db.session.add(log_entry)
    db.session.commit()
    mongo_db.transaction_logs.insert_one({
        'user_id': user.id, 'timestamp': datetime.utcnow(), 'risk_score': risk_score, 'status': status,
        'tx_hash': response_data.get('tx_hash'), 'transaction_details': data
    })
    
    return jsonify(response_data), 200

# This is a new endpoint required for the Twilio voice call
@app.route('/api/voice-response', methods=['POST'])
def voice_response():
    response = VoiceResponse()
    gather = Gather(num_digits=1, action='/api/handle-keypad', method='POST')
    gather.say("A high-risk transaction has been detected on your account. Press 1 to confirm you initiated this transaction, or press 2 to immediately block your account.")
    response.append(gather)
    response.say("We did not receive any input. Please hang up and contact support.")
    return str(response)

@app.route('/api/handle-keypad', methods=['POST'])
def handle_keypad():
    # In a real app, you'd get the user from the call SID or phone number
    # For this demo, we'll just log the action
    digits = request.form.get('Digits')
    if digits == '1':
        print("User confirmed the transaction via keypad.")
        # Logic to possibly unfreeze or verify would go here
    elif digits == '2':
        print("User requested to block account via keypad.")
        # Logic to ensure the account remains frozen
    response = VoiceResponse()
    response.say("Thank you for your response. Your action has been recorded.")
    return str(response)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)