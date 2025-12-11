# utils/encryption.py
from phe import paillier
import json
import os

class HomomorphicEncryption:
    def __init__(self):
        # Generate keys or load existing ones
        key_dir = 'keys'
        os.makedirs(key_dir, exist_ok=True)
        
        pub_key_file = os.path.join(key_dir, 'public_key.json')
        priv_key_file = os.path.join(key_dir, 'private_key.json')
        
        if os.path.exists(pub_key_file) and os.path.exists(priv_key_file):
            self.public_key, self.private_key = self._load_keys(pub_key_file, priv_key_file)
        else:
            self.public_key, self.private_key = paillier.generate_paillier_keypair()
            self._save_keys(pub_key_file, priv_key_file)
    
    def _save_keys(self, pub_file, priv_file):
        with open(pub_file, 'w') as f:
            json.dump({'n': self.public_key.n}, f)
        with open(priv_file, 'w') as f:
            json.dump({'p': self.private_key.p, 'q': self.private_key.q}, f)
    
    def _load_keys(self, pub_file, priv_file):
        with open(pub_file, 'r') as f:
            pub_data = json.load(f)
            public_key = paillier.PaillierPublicKey(n=int(pub_data['n']))
        with open(priv_file, 'r') as f:
            priv_data = json.load(f)
            private_key = paillier.PaillierPrivateKey(public_key, int(priv_data['p']), int(priv_data['q']))
        return public_key, private_key
    
    def encrypt_amount(self, amount):
        """Encrypt transaction amount"""
        encrypted = self.public_key.encrypt(float(amount))
        return {'ciphertext': str(encrypted.ciphertext()), 'exponent': encrypted.exponent}
    
    def decrypt_amount(self, encrypted_data):
        """Decrypt transaction amount"""
        from phe.paillier import EncryptedNumber
        encrypted_num = EncryptedNumber(self.public_key, int(encrypted_data['ciphertext']), encrypted_data['exponent'])
        return self.private_key.decrypt(encrypted_num)
    
    def add_encrypted(self, enc1, enc2):
        """Add two encrypted numbers"""
        from phe.paillier import EncryptedNumber
        num1 = EncryptedNumber(self.public_key, int(enc1['ciphertext']), enc1['exponent'])
        num2 = EncryptedNumber(self.public_key, int(enc2['ciphertext']), enc2['exponent'])
        result = num1 + num2
        return {'ciphertext': str(result.ciphertext()), 'exponent': result.exponent}

# Global instance
encryption_service = HomomorphicEncryption()
