# test_api.py (Improved Version)

import requests
import json
import pandas as pd
import random
import sys

# Define the base URL for the API
BASE_URL = "http://127.0.0.1:5000/api"

def run_test():
    """Main function to run the API test suite."""
    access_token = None
    
    try:
        # --- 1. Register a unique Test User ---
        print("--- 1. Registering New User ---")
        random_int = random.randint(1000, 9999)
        test_user = {
            "email": f"testuser{random_int}@example.com",
            "password": "Password123",
            "phone_number": "+1555123" + str(random_int),
            "address": "0x71C7656EC7ab88b098defB751B7401B5f6d8976F"
        }
        
        register_response = requests.post(f"{BASE_URL}/register", json=test_user)
        register_response.raise_for_status() # This will raise an error if registration fails
        print(f"✅ SUCCESS: User registered successfully. Status Code: {register_response.status_code}\n")

        # --- 2. Log In to Get the Security Token (JWT) ---
        print("--- 2. Logging In ---")
        login_response = requests.post(f"{BASE_URL}/login", json={"email": test_user["email"], "password": test_user["password"]})
        login_response.raise_for_status()
        access_token = login_response.json()['access_token']
        print(f"✅ SUCCESS: Logged in successfully. Status Code: {login_response.status_code}")
        print("Received JWT Token.\n")

        # --- 3. Prepare and Send a Secure Transaction Request ---
        print("--- 3. Submitting Transaction ---")
        headers = {"Authorization": f"Bearer {access_token}"}
        
        # Load a sample transaction from the dataset
        try:
            df = pd.read_csv('data/creditcard.csv')
            sample_row = df.iloc[500].drop('Class')
            sample_transaction = {str(k): float(v) for k, v in sample_row.items()}
        except FileNotFoundError:
            print("❌ ERROR: 'data/creditcard.csv' not found. Cannot prepare a transaction.")
            sys.exit(1) # Exit the script if the data file is missing

        transaction_response = requests.post(f"{BASE_URL}/transaction", json=sample_transaction, headers=headers)
        transaction_response.raise_for_status()
        print(f"✅ SUCCESS: Transaction processed. Status Code: {transaction_response.status_code}\n")

        # --- 4. Print the Final Result ---
        print("--- AI Analysis Result ---")
        print(json.dumps(transaction_response.json(), indent=2))
        print("--------------------------\n")
        print("🎉 Backend API test completed successfully! 🎉")

    except requests.exceptions.RequestException as e:
        print(f"\n--- ❌ ERROR ---")
        if e.response is not None:
            print(f"A server error occurred. Status Code: {e.response.status_code}")
            try:
                print(f"Server Response: {json.dumps(e.response.json(), indent=2)}")
            except json.JSONDecodeError:
                print(f"Server Response (not JSON): {e.response.text}")
        else:
            print(f"Could not connect to the API server at {BASE_URL}.")
            print("Please ensure your 'app.py' server is running in another terminal.")

if __name__ == "__main__":
    run_test()