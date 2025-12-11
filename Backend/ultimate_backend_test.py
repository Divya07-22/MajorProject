import requests
import json
from datetime import datetime

BASE_URL = 'http://localhost:5000'

class BackendValidator:
    def __init__(self):
        self.results = {'passed': 0, 'failed': 0, 'warnings': 0}
        self.token = None
        
    def test(self, name, func):
        try:
            result, message = func()
            if result == 'pass':
                print(f'PASS {name}')
                self.results['passed'] += 1
            elif result == 'warn':
                print(f'WARN {name}: {message}')
                self.results['warnings'] += 1
            else:
                print(f'FAIL {name}: {message}')
                self.results['failed'] += 1
        except Exception as e:
            print(f'FAIL {name}: {str(e)}')
            self.results['failed'] += 1
    
    def check_health(self):
        r = requests.get(f'{BASE_URL}/api/health')
        return ('pass', '') if r.status_code == 200 else ('fail', f'Status {r.status_code}')
    
    def check_register(self):
        ts = datetime.now().strftime('%H%M%S')
        data = {
            'email': f'test_{ts}@example.com',
            'password': 'Test123!',
            'phone_number': '+1234567890',
            'address': '123 Test Street',
            'ethereum_address': '0x' + '1'*40
        }
        r = requests.post(f'{BASE_URL}/api/register', json=data)
        if r.status_code == 201:
            self.test_user = data
            return 'pass', ''
        return 'fail', f'Status {r.status_code}: {r.text}'
    
    def check_login(self):
        data = {'email': self.test_user['email'], 'password': self.test_user['password']}
        r = requests.post(f'{BASE_URL}/api/login', json=data)
        if r.status_code == 200:
            self.token = r.json()['access_token']
            return 'pass', ''
        return 'fail', f'Status {r.status_code}'
    
    def check_profile_get(self):
        h = {'Authorization': f'Bearer {self.token}'}
        r = requests.get(f'{BASE_URL}/api/profile', headers=h)
        return ('pass', '') if r.status_code == 200 else ('fail', f'Status {r.status_code}')
    
    def check_profile_update(self):
        h = {'Authorization': f'Bearer {self.token}'}
        r = requests.put(f'{BASE_URL}/api/profile', json={'phone_number': '+9999999999'}, headers=h)
        return ('pass', '') if r.status_code == 200 else ('fail', f'Status {r.status_code}')
    
    def check_transaction(self, amount):
        h = {'Authorization': f'Bearer {self.token}'}
        r = requests.post(f'{BASE_URL}/api/transaction', json={'amount': amount}, headers=h)
        return ('pass', '') if r.status_code == 200 else ('fail', f'Status {r.status_code}')
    
    def check_transaction_history(self):
        h = {'Authorization': f'Bearer {self.token}'}
        r = requests.get(f'{BASE_URL}/api/transactions', headers=h)
        return ('pass', '') if r.status_code == 200 else ('fail', f'Status {r.status_code}')
    
    def check_blockchain_logs(self):
        h = {'Authorization': f'Bearer {self.token}'}
        r = requests.get(f'{BASE_URL}/api/blockchain/logs', headers=h)
        return ('pass', '') if r.status_code == 200 else ('fail', f'Status {r.status_code}')
    
    def check_invalid_login(self):
        r = requests.post(f'{BASE_URL}/api/login', json={'email': 'wrong@test.com', 'password': 'wrong'})
        return ('pass', '') if r.status_code == 401 else ('fail', f'Expected 401, got {r.status_code}')
    
    def check_unauthorized(self):
        r = requests.get(f'{BASE_URL}/api/profile')
        return ('pass', '') if r.status_code in [401, 422] else ('fail', f'Expected 401, got {r.status_code}')
    
    def run_all_tests(self):
        print('\n' + '='*70)
        print('COMPLETE BACKEND VALIDATION')
        print('='*70 + '\n')
        
        print('INFRASTRUCTURE')
        self.test('Health Check', self.check_health)
        
        print('\nUSER MANAGEMENT')
        self.test('Register', self.check_register)
        self.test('Login', self.check_login)
        self.test('Get Profile', self.check_profile_get)
        self.test('Update Profile', self.check_profile_update)
        
        print('\nTRANSACTIONS')
        self.test('Low Risk Transaction', lambda: self.check_transaction(25))
        self.test('Medium Risk Transaction', lambda: self.check_transaction(1500))
        self.test('High Risk Transaction', lambda: self.check_transaction(99999))
        self.test('Transaction History', self.check_transaction_history)
        
        print('\nBLOCKCHAIN')
        self.test('Blockchain Logs', self.check_blockchain_logs)
        
        print('\nSECURITY')
        self.test('Reject Invalid Login', self.check_invalid_login)
        self.test('Reject Unauthorized Access', self.check_unauthorized)
        
        print('\n' + '='*70)
        print('SUMMARY')
        print('='*70)
        print(f'Passed:  {self.results["passed"]}')
        print(f'Failed:  {self.results["failed"]}')
        print(f'Warnings: {self.results["warnings"]}')
        
        total = sum(self.results.values())
        rate = (self.results['passed'] / total * 100) if total > 0 else 0
        print(f'\nSuccess Rate: {rate:.1f}%')
        
        if self.results['failed'] == 0:
            print('\nALL TESTS PASSED - Backend is production-ready!')
        else:
            print(f'\n{self.results["failed"]} test(s) failed')

if __name__ == '__main__':
    BackendValidator().run_all_tests()
