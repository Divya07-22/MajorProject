# tests/test_encryption.py
import pytest
from utils.encryption import HomomorphicEncryption

@pytest.fixture
def encryption():
    """Create encryption instance"""
    return HomomorphicEncryption()

def test_encryption_initialization(encryption):
    """Test that encryption service initializes"""
    assert encryption.public_key is not None
    assert encryption.private_key is not None

def test_encrypt_decrypt_amount(encryption):
    """Test encrypting and decrypting transaction amount"""
    original_amount = 150.75
    
    # Encrypt
    encrypted = encryption.encrypt_amount(original_amount)
    assert 'ciphertext' in encrypted
    assert 'exponent' in encrypted
    
    # Decrypt
    decrypted = encryption.decrypt_amount(encrypted)
    assert abs(decrypted - original_amount) < 0.01  # Allow small floating point difference

def test_homomorphic_addition(encryption):
    """Test homomorphic addition of encrypted numbers"""
    amount1 = 100.0
    amount2 = 50.0
    
    # Encrypt both amounts
    enc1 = encryption.encrypt_amount(amount1)
    enc2 = encryption.encrypt_amount(amount2)
    
    # Add encrypted numbers
    enc_sum = encryption.add_encrypted(enc1, enc2)
    
    # Decrypt result
    decrypted_sum = encryption.decrypt_amount(enc_sum)
    
    # Check if sum is correct
    assert abs(decrypted_sum - (amount1 + amount2)) < 0.01

def test_large_amount_encryption(encryption):
    """Test encryption of large amounts"""
    large_amount = 999999.99
    
    encrypted = encryption.encrypt_amount(large_amount)
    decrypted = encryption.decrypt_amount(encrypted)
    
    assert abs(decrypted - large_amount) < 0.01
