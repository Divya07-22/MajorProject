import requests
import json
from datetime import datetime

BASE_URL = 'http://localhost:5000'
results = []

def test(name, method, endpoint, data=None, headers=None, expect_status=200):
    try:
        url = f'{BASE_URL}{endpoint}'
        if method == 'GET':
            resp = requests.get(url, headers=headers)
        elif method == 'POST':
            resp = requests.post(url, json=data, headers=headers)
        elif method == 'PUT':
            resp = requests.put(url, json=data, headers=headers)
        
        status = resp.status_code
        success = (status == expect_status)
        results.append({
            'test': name,
            'status': status,
            'expected': expect_status,
            'result': ' PASS' if success else ' FAIL',
            'response': resp.json() if resp.content else {}
        })
        return resp, success
    except Exception as e:
        results.append({
            'test': name,
            'status': 'ERROR',
            'expected': expect_status,
            'result': ' FAIL',
            'response': str(e)
        })
        return None, False

print('='*70)
print('COMPREHENSIVE BACKEND API TEST SUITE')
print('='*70)

# Test 1: Health Check
print('\n[1] Testing Health Check...')
test('Health Check', 'GET', '/api/health')

# Test 2: Registration
print('[2] Testing User Registration...')
timestamp = datetime.now().strftime('%H%M%S')
user_data = {
    'username': f'testuser_{timestamp}',
    'email': f'test_{timestamp}@example.com',
    'password': 'SecurePass123!',
    'phone_number': '+1234567890',
    'address': '123 Test St',
    'ethereum_address': '0x1234567890123456789012345678901234567890'
}
resp, success = test('User Registration', 'POST', '/api/register', user_data, expect_status=201)

if not success:
    print(' Registration failed! Stopping tests.')
    exit(1)

# Test 3: Login
print('[3] Testing User Login...')
login_data = {'email': user_data['email'], 'password': user_data['password']}
resp, success = test('User Login', 'POST', '/api/login', login_data)

if not success:
    print(' Login failed! Stopping tests.')
    exit(1)

token = resp.json()['access_token']
headers = {'Authorization': f'Bearer {token}'}

# Test 4: Get User Profile
print('[4] Testing Get Profile...')
test('Get Profile', 'GET', '/api/profile', headers=headers)

# Test 5: Update Profile
print('[5] Testing Update Profile...')
update_data = {'phone_number': '+9876543210'}
test('Update Profile', 'PUT', '/api/profile', update_data, headers=headers)

# Test 6: Simple Transaction (Low Risk)
print('[6] Testing Low Risk Transaction...')
tx_data = {'amount': 50.0}
test('Low Risk Transaction', 'POST', '/api/transaction', tx_data, headers=headers)

# Test 7: Complex Transaction with All Fields
print('[7] Testing Transaction with All Fields...')
tx_full = {
    'amount': 1200.0,
    'merchant': 'Amazon',
    'location': 'Seattle, WA',
    'transaction_type': 'online'
}
test('Full Transaction', 'POST', '/api/transaction', tx_full, headers=headers)

# Test 8: High Risk Transaction (should trigger alerts)
print('[8] Testing High Risk Transaction...')
tx_high = {'amount': 50000.0}
test('High Risk Transaction', 'POST', '/api/transaction', tx_high, headers=headers)

# Test 9: Get Transaction History
print('[9] Testing Transaction History...')
test('Transaction History', 'GET', '/api/transactions', headers=headers)

# Test 10: Get Blockchain Logs
print('[10] Testing Blockchain Logs...')
test('Blockchain Logs', 'GET', '/api/blockchain/logs', headers=headers)

# Test 11: Invalid Login (should fail)
print('[11] Testing Invalid Login...')
bad_login = {'email': 'wrong@test.com', 'password': 'wrong'}
test('Invalid Login', 'POST', '/api/login', bad_login, expect_status=401)

# Test 12: Protected Route without Token (should fail)
print('[12] Testing Unauthorized Access...')
test('Unauthorized Profile', 'GET', '/api/profile', expect_status=401)

# Test 13: Transaction without Token (should fail)
print('[13] Testing Transaction without Auth...')
test('Unauthorized Transaction', 'POST', '/api/transaction', {'amount': 100}, expect_status=401)

print('\n' + '='*70)
print('TEST RESULTS SUMMARY')
print('='*70)

pass_count = sum(1 for r in results if '' in r['result'])
fail_count = len(results) - pass_count

for r in results:
    print(f"{r['result']} {r['test']:40s} Status: {r['status']}/{r['expected']}")

print(f'\nTotal: {len(results)} tests |  Passed: {pass_count} |  Failed: {fail_count}')

if fail_count == 0:
    print('\n ALL TESTS PASSED! Backend is fully functional!')
else:
    print(f'\n {fail_count} test(s) failed. Check logs above.')

# Save detailed results
with open('test_results.json', 'w') as f:
    json.dump(results, f, indent=2)
    
print('\nDetailed results saved to test_results.json')
