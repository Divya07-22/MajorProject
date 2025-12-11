import requests
import json

BASE_URL = 'http://localhost:5000'

print(' Testing Fraud Detection API...\n')

# Test 1: Health Check
print('1. Testing /api/health...')
try:
    response = requests.get(f'{BASE_URL}/api/health')
    print(f'   Status: {response.status_code}')
    print(f'   Response: {response.json()}\n')
except Exception as e:
    print(f'   Error: {e}\n')

# Test 2: Register User
print('2. Testing /api/register...')
test_user = {
    'username': 'testuser',
    'email': 'test@example.com',
    'password': 'Test123!@#',
    'phone_number': '+1234567890'
}
try:
    response = requests.post(f'{BASE_URL}/api/register', json=test_user)
    print(f'   Status: {response.status_code}')
    print(f'   Response: {response.json()}\n')
except Exception as e:
    print(f'   Error: {e}\n')

# Test 3: Login
print('3. Testing /api/login...')
login_data = {
    'email': 'test@example.com',
    'password': 'Test123!@#'
}
try:
    response = requests.post(f'{BASE_URL}/api/login', json=login_data)
    print(f'   Status: {response.status_code}')
    print(f'   Response: {response.json()}\n')
except Exception as e:
    print(f'   Error: {e}\n')

print(' API Tests Complete!')
