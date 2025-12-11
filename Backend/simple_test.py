import requests
from datetime import datetime

BASE_URL = 'http://localhost:5000'

# Register
user = {
    'username': f'test_{datetime.now().strftime("%H%M%S")}',
    'email': f't_{datetime.now().strftime("%H%M%S")}@ex.com',
    'password': 'Pass123!',
    'phone_number': '+1234567890',
    'address': '123 St'
}
requests.post(f'{BASE_URL}/api/register', json=user)

# Login
login = {'email': user['email'], 'password': user['password']}
response = requests.post(f'{BASE_URL}/api/login', json=login)
token = response.json()['access_token']

# Simple transaction with ONLY amount
headers = {'Authorization': f'Bearer {token}'}
tx = {'amount': 100.00}

response = requests.post(f'{BASE_URL}/api/transaction', json=tx, headers=headers)
print(f'Status: {response.status_code}')
print(f'Response: {response.json()}')
