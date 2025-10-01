# test_api.py
import requests
import json
import pandas as pd
import random

# Define the base URL for the API
BASE_URL = "http://127.0.0.1:5000/api"

# --- 1. Define a Test User ---
# We use a random number to ensure the user is unique each time
random_int = random.randint(1000, 9999)
test_user = {
    "email": f"testuser{random_int}@example.com",
    "password": "password123",
    "phone_number": "+1555123" + str(random_int),
    "address": "0x71C7656EC7ab88b098defB751B7401B5f6d8976F" # Example address from Ganache
}

access_token = None

try:
    # --- 2. Register the Test User ---
    print("--- 1. Registering a new test user...")
    requests.post(f"{BASE_URL}/register", json=test_user)

    # --- 3. Log In to Get the Security Token (JWT) ---
    print("--- 2. Logging in to get a security token...")
    login_response = requests.post(f"{BASE_URL}/login", json={"email": test_user["email"], "password": test_user["password"]})
    login_response.raise_for_status()
    access_token = login_response.json()['access_token']
    print("   -> Successfully received token.")

    # --- 4. Prepare the Authorization Header ---
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    # --- 5. Prepare the High-Risk Transaction Data ---
    print("--- 3. Preparing a high-risk transaction...")
    df = pd.read_csv('data/creditcard.csv')
    
    # This new code is more explicit about converting to simple Python types
    sample_row = df.iloc[500].drop('Class')
    sample_transaction = {}
    for col_name, value in sample_row.items():
        sample_transaction[str(col_name)] = float(value)
    
    # --- 6. Send the Secure Transaction Request ---
    print("--- 4. Sending the secure transaction to the backend...")
    transaction_response = requests.post(f"{BASE_URL}/transaction", json=sample_transaction, headers=headers)
    transaction_response.raise_for_status()

    # --- 7. Print the Final Result ---
    print("\n--- ✅ API Response Received ---")
    print(json.dumps(transaction_response.json(), indent=2))
    print("------------------------------")

except requests.exceptions.RequestException as e:
    print(f"\n--- ❌ ERROR ---")
    if e.response:
        print(f"Status Code: {e.response.status_code}")
        print(f"Response: {e.response.text}")
    else:
        print(f"Could not connect to the API server at {BASE_URL}.")
        print("Please ensure your 'app.py' server is running in another terminal.")

except FileNotFoundError:
    print("Error: 'data/creditcard.csv' not found. Cannot run a realistic test.")