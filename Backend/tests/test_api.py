# test_api.py - Enhanced API Testing Script
import requests
import json
import pandas as pd
import random
import sys
import time

# Base URL for the API
BASE_URL = "http://127.0.0.1:5000/api"

# Colors for terminal output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

def print_success(message):
    print(f"{GREEN}✅ {message}{RESET}")

def print_error(message):
    print(f"{RED}❌ {message}{RESET}")

def print_info(message):
    print(f"{BLUE}ℹ️  {message}{RESET}")

def print_warning(message):
    print(f"{YELLOW}⚠️  {message}{RESET}")

def print_section(title):
    print(f"\n{BLUE}{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}{RESET}\n")

# Test 1: Health Check
def test_health_check():
    print_section("TEST 1: Health Check")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            data = response.json()
            print_success(f"Health check passed - Status: {data.get('status')}")
            print_info(f"Services: {json.dumps(data.get('services', {}), indent=2)}")
            return True
        else:
            print_error(f"Health check failed - Status Code: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Health check error: {e}")
        print_warning("Make sure the server is running: python app.py")
        return False

# Test 2: User Registration
def test_user_registration():
    print_section("TEST 2: User Registration")
    try:
        random_int = random.randint(1000, 9999)
        test_user = {
            "email": f"testuser{random_int}@example.com",
            "password": "SecurePass123!",
            "phone_number": f"+1555{random_int:04d}",
            "address": "0x71C7656EC7ab88b098defB751B7401B5f6d8976F"
        }
        
        print_info(f"Registering user: {test_user['email']}")
        response = requests.post(f"{BASE_URL}/register", json=test_user)
        
        if response.status_code == 201:
            print_success("User registered successfully")
            return test_user
        else:
            print_error(f"Registration failed - Status: {response.status_code}")
            print_error(f"Response: {response.text}")
            return None
    except Exception as e:
        print_error(f"Registration error: {e}")
        return None

# Test 3: User Login
def test_user_login(user):
    print_section("TEST 3: User Login")
    try:
        login_data = {
            "email": user["email"],
            "password": user["password"]
        }
        
        print_info(f"Logging in as: {user['email']}")
        response = requests.post(f"{BASE_URL}/login", json=login_data)
        
        if response.status_code == 200:
            data = response.json()
            token = data.get('access_token')
            print_success("Login successful")
            print_info(f"JWT Token received (length: {len(token)})")
            return token
        else:
            print_error(f"Login failed - Status: {response.status_code}")
            print_error(f"Response: {response.text}")
            return None
    except Exception as e:
        print_error(f"Login error: {e}")
        return None

# Test 4: Transaction Submission (Low Risk)
def test_transaction_low_risk(token):
    print_section("TEST 4: Transaction Submission (Low Risk)")
    try:
        headers = {"Authorization": f"Bearer {token}"}
        
        # Low risk transaction (small amount)
        transaction_data = {"amount": 25.50}
        
        print_info(f"Submitting transaction: ${transaction_data['amount']}")
        response = requests.post(f"{BASE_URL}/transaction", json=transaction_data, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            print_success("Transaction processed successfully")
            print_info(f"Risk Score: {data.get('risk_score', 0)*100:.2f}%")
            print_info(f"Status: {data.get('status')}")
            return data
        else:
            print_error(f"Transaction failed - Status: {response.status_code}")
            print_error(f"Response: {response.text}")
            return None
    except Exception as e:
        print_error(f"Transaction error: {e}")
        return None

# Test 5: Transaction Submission (High Risk)
def test_transaction_high_risk(token):
    print_section("TEST 5: Transaction Submission (High Risk)")
    try:
        headers = {"Authorization": f"Bearer {token}"}
        
        # Try to load dataset for realistic high-risk transaction
        try:
            df = pd.read_csv('data/creditcard.csv')
            # Get a fraud sample
            fraud_samples = df[df['Class'] == 1]
            if len(fraud_samples) > 0:
                sample = fraud_samples.iloc[0].drop('Class').to_dict()
                transaction_data = {str(k): float(v) for k, v in sample.items()}
                print_info("Using real fraud sample from dataset")
            else:
                transaction_data = {"amount": 9999.99}
                print_warning("No fraud samples in dataset, using large amount")
        except FileNotFoundError:
            transaction_data = {"amount": 9999.99}
            print_warning("Dataset not found, using large amount")
        
        print_info(f"Submitting potentially fraudulent transaction")
        response = requests.post(f"{BASE_URL}/transaction", json=transaction_data, headers=headers)
        
        if response.status_code in [200, 403]:
            data = response.json()
            if response.status_code == 403:
                print_warning("Account frozen due to high risk!")
            print_info(f"Risk Score: {data.get('risk_score', 0)*100:.2f}%")
            print_info(f"Status: {data.get('status')}")
            if data.get('tx_hash'):
                print_success(f"Blockchain TX: {data.get('tx_hash')}")
            return data
        else:
            print_error(f"Transaction failed - Status: {response.status_code}")
            print_error(f"Response: {response.text}")
            return None
    except Exception as e:
        print_error(f"Transaction error: {e}")
        return None

# Test 6: Get Transaction History
def test_get_transactions(token):
    print_section("TEST 6: Get Transaction History")
    try:
        headers = {"Authorization": f"Bearer {token}"}
        
        print_info("Fetching transaction history...")
        response = requests.get(f"{BASE_URL}/transactions", headers=headers)
        
        if response.status_code == 200:
            transactions = response.json()
            print_success(f"Retrieved {len(transactions)} transactions")
            
            if transactions:
                print_info("Recent transactions:")
                for txn in transactions[:3]:  # Show first 3
                    print(f"  - ID: {txn['id']}, Risk: {txn['risk_score']*100:.1f}%, Status: {txn['status']}")
            return transactions
        else:
            print_error(f"Failed to get transactions - Status: {response.status_code}")
            return None
    except Exception as e:
        print_error(f"Get transactions error: {e}")
        return None

# Test 7: Get Blockchain Logs
def test_blockchain_logs(token):
    print_section("TEST 7: Get Blockchain Logs")
    try:
        headers = {"Authorization": f"Bearer {token}"}
        
        print_info("Fetching blockchain logs...")
        response = requests.get(f"{BASE_URL}/blockchain/logs", headers=headers)
        
        if response.status_code == 200:
            logs = response.json()
            print_success(f"Retrieved {len(logs)} blockchain logs")
            
            if logs:
                print_info("Recent blockchain transactions:")
                for log in logs[:3]:
                    print(f"  - TX: {log['tx_hash'][:16]}..., Block: {log['block_number']}")
            return logs
        else:
            print_warning(f"No blockchain logs found - Status: {response.status_code}")
            return None
    except Exception as e:
        print_error(f"Blockchain logs error: {e}")
        return None

# Test 8: Invalid Login
def test_invalid_login():
    print_section("TEST 8: Invalid Login (Security Test)")
    try:
        invalid_data = {
            "email": "nonexistent@example.com",
            "password": "WrongPassword123"
        }
        
        print_info("Attempting login with invalid credentials...")
        response = requests.post(f"{BASE_URL}/login", json=invalid_data)
        
        if response.status_code == 401:
            print_success("Security test passed - Invalid login rejected")
            return True
        else:
            print_error(f"Security issue - Expected 401, got {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Invalid login test error: {e}")
        return False

# Test 9: Unauthorized Access
def test_unauthorized_access():
    print_section("TEST 9: Unauthorized Access (Security Test)")
    try:
        print_info("Attempting to access protected endpoint without token...")
        response = requests.get(f"{BASE_URL}/transactions")
        
        if response.status_code == 401:
            print_success("Security test passed - Unauthorized access blocked")
            return True
        else:
            print_error(f"Security issue - Expected 401, got {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Unauthorized access test error: {e}")
        return False

# Main test runner
def run_all_tests():
    print(f"\n{BLUE}{'='*60}")
    print(f"  🚀 FRAUD DETECTION API - COMPREHENSIVE TEST SUITE")
    print(f"{'='*60}{RESET}\n")
    
    print_info(f"Target: {BASE_URL}")
    print_info(f"Time: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    results = {
        "passed": 0,
        "failed": 0,
        "total": 9
    }
    
    # Test 1: Health Check
    if test_health_check():
        results["passed"] += 1
    else:
        results["failed"] += 1
        print_error("\n❌ Server is not running! Please start it with: python app.py")
        sys.exit(1)
    
    # Test 2: User Registration
    user = test_user_registration()
    if user:
        results["passed"] += 1
    else:
        results["failed"] += 1
    
    # Test 3: User Login
    token = None
    if user:
        token = test_user_login(user)
        if token:
            results["passed"] += 1
        else:
            results["failed"] += 1
    
    # Test 4: Low Risk Transaction
    if token:
        if test_transaction_low_risk(token):
            results["passed"] += 1
        else:
            results["failed"] += 1
    
    # Test 5: High Risk Transaction
    if token:
        if test_transaction_high_risk(token):
            results["passed"] += 1
        else:
            results["failed"] += 1
    
    # Test 6: Transaction History
    if token:
        if test_get_transactions(token):
            results["passed"] += 1
        else:
            results["failed"] += 1
    
    # Test 7: Blockchain Logs
    if token:
        if test_blockchain_logs(token):
            results["passed"] += 1
        else:
            results["failed"] += 1
    
    # Test 8: Invalid Login
    if test_invalid_login():
        results["passed"] += 1
    else:
        results["failed"] += 1
    
    # Test 9: Unauthorized Access
    if test_unauthorized_access():
        results["passed"] += 1
    else:
        results["failed"] += 1
    
    # Final Results
    print_section("TEST SUMMARY")
    print(f"Total Tests: {results['total']}")
    print(f"{GREEN}Passed: {results['passed']}{RESET}")
    print(f"{RED}Failed: {results['failed']}{RESET}")
    
    success_rate = (results['passed'] / results['total']) * 100
    
    if success_rate == 100:
        print(f"\n{GREEN}{'='*60}")
        print(f"  🎉 ALL TESTS PASSED! Backend is fully functional!")
        print(f"{'='*60}{RESET}\n")
    elif success_rate >= 70:
        print(f"\n{YELLOW}{'='*60}")
        print(f"  ⚠️  Most tests passed ({success_rate:.0f}%), but some need attention")
        print(f"{'='*60}{RESET}\n")
    else:
        print(f"\n{RED}{'='*60}")
        print(f"  ❌ Multiple failures detected ({success_rate:.0f}% passed)")
        print(f"{'='*60}{RESET}\n")
    
    return success_rate == 100

if __name__ == "__main__":
    try:
        success = run_all_tests()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print(f"\n\n{YELLOW}Tests interrupted by user{RESET}")
        sys.exit(1)
    except Exception as e:
        print(f"\n{RED}Fatal error: {e}{RESET}")
        sys.exit(1)
