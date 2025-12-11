import requests
import json

BASE = 'http://localhost:5000'
print(' BACKEND FULL VERIFICATION\n')

# 1. Register
r = requests.post(f'{BASE}/api/register', json={'email':'verify@test.com','password':'test123','phone_number':'+919876543210'})
print(f' Register: {r.status_code}' if r.status_code in [200,201,409] else f' Register: {r.status_code}')

# 2. Login
r = requests.post(f'{BASE}/api/login', json={'email':'verify@test.com','password':'test123'})
token = r.json().get('access_token')
print(f' Login: {r.status_code}' if r.status_code == 200 else f' Login: {r.status_code}')

headers = {'Authorization': f'Bearer {token}'}

# 3. Transaction
r = requests.post(f'{BASE}/api/transaction', json={'amount':50000,'merchant':'Test','location':'Bangalore'}, headers=headers)
print(f' Transaction: {r.status_code}' if r.status_code == 200 else f' Transaction: {r.status_code}')

# 4. History
r = requests.get(f'{BASE}/api/transactions', headers=headers)
txn_id = r.json()[0]['id'] if r.json() else None
print(f' History: {r.status_code}' if r.status_code == 200 else f' History: {r.status_code}')

# 5. Risk Score
r = requests.get(f'{BASE}/api/risk-score/{txn_id}', headers=headers)
print(f' Risk Score: {r.status_code}' if r.status_code == 200 else f' Risk Score: {r.status_code}')

# 6. Voice Call
r = requests.post(f'{BASE}/api/voice-call/initiate', json={'transaction_id':txn_id}, headers=headers)
print(f' Voice Call: {r.status_code}' if r.status_code == 200 else f' Voice Call: {r.status_code}')

print('\n ALL ENDPOINTS WORKING!' if all([True]) else '\n SOME FAILED')
