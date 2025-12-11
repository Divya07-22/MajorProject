import requests
import json

BASE_URL = 'http://localhost:5000'

# Test registration with verbose output
data = {
    'email': 'test_debug@example.com',
    'password': 'Test123!',
    'phone_number': '+1234567890',
    'ethereum_address': '0x1111111111111111111111111111111111111111'
}

print('Testing registration with data:')
print(json.dumps(data, indent=2))

r = requests.post(f'{BASE_URL}/api/register', json=data)

print(f'\nStatus: {r.status_code}')
print(f'Response: {r.text}')

if r.status_code == 201:
    print('\nSUCCESS!')
else:
    print('\nFAILED - Check what fields are missing!')
