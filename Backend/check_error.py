import requests
from datetime import datetime

BASE_URL = 'http://localhost:5000'

# Quick login with existing user
test_user = {'email': 'test_20251005120603@example.com', 'password': 'SecurePass123!@#'}
response = requests.post(f'{BASE_URL}/api/login', json=test_user)
token = response.json()['access_token']

# Test transaction with detailed error
headers = {'Authorization': f'Bearer {token}'}
transaction = {
    'amount': 5000.00,
    'merchant': 'Amazon',
    'location': 'New York',
    'transaction_type': 'online'
}

response = requests.post(f'{BASE_URL}/api/transaction', json=transaction, headers=headers)
print(f'Status: {response.status_code}')
print(f'Response: {response.text}')
