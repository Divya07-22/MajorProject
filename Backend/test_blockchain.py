import requests

BASE = 'http://localhost:5000'

requests.post(f'{BASE}/api/register', json={
    'email':'blockchain_test@example.com',
    'password':'Test@1234',
    'phone_number':'+919876543210',
    'address':'0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb1'
})

r = requests.post(f'{BASE}/api/login', json={'email':'blockchain_test@example.com','password':'Test@1234'})
print(f'Login: {r.status_code}')
token = r.json()['access_token']

# HIGH RISK - USE Amount (UPPERCASE)
high_risk_txn = {
    'Amount': 999999,
    'V1': 10.5, 'V2': -8.3, 'V3': 15.2, 'V4': 12.1, 'V5': -9.4, 
    'V6': 11.8, 'V7': -7.6, 'V8': 13.2, 'V9': -10.1, 'V10': 14.5, 
    'V11': -11.2, 'V12': 9.8, 'V13': -12.4, 'V14': 10.9, 'V15': -8.7,
    'V16': 13.6, 'V17': -9.2, 'V18': 11.4, 'V19': -10.8, 'V20': 12.7,
    'V21': -9.5, 'V22': 10.3, 'V23': -11.7, 'V24': 13.1, 'V25': -8.9,
    'V26': 12.2, 'V27': -10.4, 'V28': 14.8, 'Time': 50000
}

r = requests.post(f'{BASE}/api/transaction', json=high_risk_txn, headers={'Authorization': f'Bearer {token}'})
print(f'\n HIGH RISK TEST:')
print(r.json())
print(f'\nStatus: {r.status_code}')
