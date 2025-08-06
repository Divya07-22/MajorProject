import json
import subprocess
import pandas as pd
import xgboost as xgb
from flask import Flask, request, jsonify
from web3 import Web3

app = Flask(__name__)
ganache_url = "http://127.0.0.1:7545" 
web3 = Web3(Web3.HTTPProvider(ganache_url))
if not web3.is_connected(): raise Exception("ERROR: Could not connect to Ganache.")

# --- PASTE YOUR DEPLOYED **FRAUDMITIGATOR** ADDRESS AND ABI HERE ---
contract_address = "YOUR_DEPLOYED_FRAUDMITIGATOR_ADDRESS" 
contract_abi = [ /* PASTE ABI FROM build/contracts/FraudMitigator.json */ ]
# ---------------------------------------------------------

mitigator_contract = web3.eth.contract(address=contract_address, abi=contract_abi)
web3.eth.default_account = web3.eth.accounts[0]
model_path = 'trained_models/xgb_risk_model.json'

@app.route('/assess', methods=['POST'])
def assess_transaction():
    try:
        # 1. Get transaction data and predict with AI
        transaction_data = request.json
        df = pd.DataFrame([transaction_data])
        xgb_model = xgb.XGBClassifier(); xgb_model.load_model(model_path)
        risk_score = int(xgb_model.predict_proba(df)[0][1] * 100)
        print(f"AI Risk Score: {risk_score}%")

        # 2. Define risk thresholds
        HIGH_RISK_THRESHOLD = 85
        MEDIUM_RISK_THRESHOLD = 60
        
        # Default empty proof for non-high-risk cases
        proof = {'proof': {'a': [0,0], 'b': [[0,0],[0,0]], 'c': [0,0]}, 'inputs': [HIGH_RISK_THRESHOLD]} # Use threshold as default input

        # 3. If risk is high, generate a real ZKP using the local .exe
        if risk_score >= HIGH_RISK_THRESHOLD:
            print("High risk. Generating ZKP...")
            # Use the local zokrates.exe for Windows
            subprocess.run([".\\zokrates.exe", "compute-witness", "-a", str(risk_score), str(HIGH_RISK_THRESHOLD)], check=True)
            subprocess.run([".\\zokrates.exe", "generate-proof"], check=True)
            with open('proof.json', 'r') as f: proof = json.load(f)
            print("ZKP Generated.")

        # 4. Call the smart contract with the risk score and proof
        if risk_score >= MEDIUM_RISK_THRESHOLD:
            print("Submitting transaction to smart contract...")
            tx_hash = mitigator_contract.functions.executeResponse(
                risk_score,
                web3.eth.accounts[1], # Example user account that would be frozen
                "TX_ID_" + str(pd.Timestamp.now().timestamp()),
                proof['inputs'],
                proof['proof']['a'],
                proof['proof']['b'],
                proof['proof']['c']
            ).transact()
            receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
            
            if risk_score >= HIGH_RISK_THRESHOLD:
                status = "High Risk: Account Frozen & Reported to Blockchain"
            else:
                status = "Medium Risk: MFA Triggered on Blockchain"
                
            return jsonify({ "status": status, "tx_hash": receipt.transactionHash.hex() })
        else:
            return jsonify({ "status": "Low Risk - Approved" })
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000)