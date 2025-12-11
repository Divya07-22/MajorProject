# scripts/validate_env.py
import os
import sys
from dotenv import load_dotenv

load_dotenv()

REQUIRED_VARS = [
    'SECRET_KEY',
    'JWT_SECRET_KEY',
    'DATABASE_URL',
    'MONGO_URI',
    'INFURA_URL',
    'SIGNER_PRIVATE_KEY',
    'FRAUD_MITIGATOR_CONTRACT_ADDRESS',
    'FRAUD_LEDGER_CONTRACT_ADDRESS',
    'TWILIO_ACCOUNT_SID',
    'TWILIO_AUTH_TOKEN',
    'TWILIO_PHONE_NUMBER'
]

def validate_environment():
    missing_vars = []
    
    for var in REQUIRED_VARS:
        if not os.environ.get(var):
            missing_vars.append(var)
    
    if missing_vars:
        print("❌ ERROR: Missing required environment variables:")
        for var in missing_vars:
            print(f"  - {var}")
        print("\nPlease set these variables in your .env file")
        sys.exit(1)
    
    print("✅ All required environment variables are set!")
    print("\n🔍 Validating values...")
    
    # Check database URL format
    if not os.environ.get('DATABASE_URL').startswith('postgresql://'):
        print("⚠️  WARNING: DATABASE_URL should start with 'postgresql://'")
    
    # Check MongoDB URI format
    if not os.environ.get('MONGO_URI').startswith('mongodb://'):
        print("⚠️  WARNING: MONGO_URI should start with 'mongodb://'")
    
    # Check private key length
    if len(os.environ.get('SIGNER_PRIVATE_KEY')) != 64:
        print("⚠️  WARNING: SIGNER_PRIVATE_KEY should be 64 characters (32 bytes)")
    
    print("\n✅ Environment validation complete!")

if __name__ == "__main__":
    validate_environment()
