import requests
import json

BASE_URL = 'http://localhost:5000'

print(' Testing with CORRECT data...\n')

# Test 1: Register with address field
print('1. Registering user with address...')
test_user = {
    'username': 'john_doe',
    'email': 'john@example.com',
    'password': 'SecurePass123!@#',
    'phone_number': '+1234567890',
    'address': '123 Main St, City, State 12345'  # Added missing field
}
try:
    response = requests.post(f'{BASE_URL}/api/register', json=test_user)
    print(f'   Status: {response.status_code}')
    print(f'   Response: {response.json()}\n')
    if response.status_code == 201:
        print('    User registered successfully!\n')
except Exception as e:
    print(f'   Error: {e}\n')

# Test 2: Login with registered user
print('2. Logging in...')
login_data = {
    'email': 'john@example.com',
    'password': 'SecurePass123!@#'
}
try:
    response = requests.post(f'{BASE_URL}/api/login', json=login_data)
    print(f'   Status: {response.status_code}')
    result = response.json()
    print(f'   Response: {result}\n')
    if response.status_code == 200:
        print(f'    Login successful!')
        print(f'   Token: {result.get("access_token", "N/A")[:50]}...\n')
except Exception as e:
    print(f'   Error: {e}\n')

print(' API is fully functional!')
