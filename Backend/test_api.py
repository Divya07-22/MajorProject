# test_api.py
import requests
import json
import pandas as pd

API_URL = "http://127.0.0.1:5000/assess"

print("--- Testing the Fraud Prevention API ---")

# We create a sample transaction that will be classified as high-risk
# by the AI model to ensure the blockchain path is triggered.
try:
    df = pd.read_csv('data/creditcard.csv')
    # Take a sample row from the original data
    sample_transaction = df.iloc[500].drop('Class').to_dict()
    
    # Manually add high-risk scores from our other models
    sample_transaction['anomaly_score'] = -0.6  # A very low score from Isolation Forest is a red flag
    sample_transaction['lstm_error'] = 0.9      # A high reconstruction error from LSTM is a red flag
    sample_transaction['gnn_pred'] = 1          # 1 means the GNN predicts fraud

except FileNotFoundError:
    print("Error: 'data/creditcard.csv' not found. Cannot run a realistic test.")
    exit()

print("\nSending High-Risk Transaction to API...")
try:
    # Send the transaction data as a JSON payload
    response = requests.post(API_URL, json=sample_transaction)
    response.raise_for_status() # Raise an error for bad status codes (like 404 or 500)
    
    # Print the JSON response from the server
    print("\n--- API Response Received ---")
    print(json.dumps(response.json(), indent=2))
    print("-------------------------")

except requests.exceptions.RequestException as e:
    print(f"\nERROR: Could not connect to the API server.")
    print("Please ensure your 'app.py' server is running in another terminal.")