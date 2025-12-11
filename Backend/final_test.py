import requests
from datetime import datetime

BASE_URL = 'http://localhost:5000'

print(' Complete test with ALL fields...\n')

# Register new user
test_user = {
    'username': f'user_{datetime.now().strftime("%H%M%S")}',
    'email': f'newtest_{datetime.now().strftime("%H%M%S")}@example.com',
    'password': 'Pass123!@#',
    'phone_number': '+1234567890',
    'address': '123 Main St'
}

response = requests.post(f'{BASE_URL}/api/register', json=test_user)
print(f' Registration: {response.status_code}')

# Login
login_data = {'email': test_user['email'], 'password': test_user['password']}
response = requests.post(f'{BASE_URL}/api/login', json=login_data)
token = response.json()['access_token']
print(f' Login: {response.status_code}')

# Submit transaction WITH ALL FIELDS
headers = {'Authorization': f'Bearer {token}'}
transaction = {
    'amount': 7500.00,
    'merchant': 'Best Buy',
    'location': 'Los Angeles, CA',
    'transaction_type': 'in-store'
}

response = requests.post(f'{BASE_URL}/api/transaction', json=transaction, headers=headers)
print(f'\n Transaction Status: {response.status_code}')

if response.status_code == 200:
    result = response.json()
    print(f' Transaction ID: {result.get("transaction_id")}')
    print(f' Fraud Score: {result.get("fraud_score")}')
    print(f' Status: {result.get("status")}')
    
    # Verify in database
    import psycopg2
    conn = psycopg2.connect(host='localhost', port=5432, database='fraud_prevention_db', user='postgres', password='postgres')
    cur = conn.cursor()
    cur.execute('SELECT amount, merchant, location, transaction_type, risk_score FROM transaction_log ORDER BY id DESC LIMIT 1')
    row = cur.fetchone()
    print(f'\n Database Verification:')
    print(f'   Amount: ')
    print(f'   Merchant: {row[1]}')
    print(f'   Location: {row[2]}')
    print(f'   Type: {row[3]}')
    print(f'   Risk Score: {row[4]:.2f}')
    print('\n ALL FIELDS STORED SUCCESSFULLY!')
else:
    print(f' Error: {response.text}')
