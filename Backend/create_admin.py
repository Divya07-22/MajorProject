from app import app, db, User
from werkzeug.security import generate_password_hash
from zkp_handler import zkp_handler
from did_handler import did_handler
import json

with app.app_context():
    # Check if admin already exists
    existing = User.query.filter_by(email='deepthi@gmail.com').first()
    if existing:
        print("❌ Admin already exists!")
    else:
        new_admin = User(
            email='deepthi@gmail.com',
            phone_number='+919876543210',
            ethereum_address='0xa3e5B78bf69AF6339E9daB69ad922c2c3985a0F9',
            role='admin'
        )
        new_admin.password_hash = generate_password_hash('Deepthi@123')
        
        db.session.add(new_admin)
        db.session.commit()
        
        identity_proof = zkp_handler.create_identity_proof(new_admin.id, new_admin.ethereum_address)
        new_admin.zkp_identity_proof = identity_proof['commitment']
        
        did_document = did_handler.create_did_document(new_admin.id, new_admin.ethereum_address, new_admin.email)
        new_admin.did_document = json.dumps(did_document)
        
        db.session.commit()
        
        print(f"✅ Admin created: {new_admin.email}")
        print(f"✅ Password: Deepthi@123")
