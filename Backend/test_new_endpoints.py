import requests

BASE_URL = 'http://localhost:5000'

print("="*70)
print("TESTING NEW ENDPOINTS")
print("="*70)

# 1. Register and login
data = {
    'email': 'test_new@example.com',
    'password': 'Test123!',
    'phone_number': '+1234567890',
    'address': '123 Test St',
    'ethereum_address': '0x' + '1'*40
}
r = requests.post(f'{BASE_URL}/api/register', json=data)
print(f"\n1. Register: {r.status_code}")

r = requests.post(f'{BASE_URL}/api/login', json={'email': data['email'], 'password': data['password']})
token = r.json()['access_token']
headers = {'Authorization': f'Bearer {token}'}
print(f"2. Login: {r.status_code}")

# 2. Create transaction
r = requests.post(f'{BASE_URL}/api/transaction', json={'amount': 5000}, headers=headers)
txn_data = r.json()
txn_id = txn_data.get('transaction_id')
print(f"3. Transaction created: {r.status_code}, ID: {txn_id}")

# 3. Test GET /api/risk-score/<id>
if txn_id:
    r = requests.get(f'{BASE_URL}/api/risk-score/{txn_id}', headers=headers)
    print(f"4. GET /api/risk-score/{txn_id}: {r.status_code}")
    if r.status_code == 200:
        print(f"    Risk Score Endpoint Working!")
        print(f"   Data: {r.json()}")
    else:
        print(f"    Error: {r.text}")

# 4. Test POST /api/voice-call/initiate
if txn_id:
    r = requests.post(f'{BASE_URL}/api/voice-call/initiate', json={'transaction_id': txn_id}, headers=headers)
    print(f"5. POST /api/voice-call/initiate: {r.status_code}")
    if r.status_code == 200:
        print(f"    Voice Call Endpoint Working!")
        print(f"   Response: {r.json()}")
    else:
        print(f"    Error: {r.text}")

print("\n" + "="*70)
print("ALL NEW ENDPOINTS TESTED!")
print("="*70)
