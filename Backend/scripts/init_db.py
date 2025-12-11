# scripts/init_db.py
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, db, User
from werkzeug.security import generate_password_hash

def initialize_database():
    with app.app_context():
        print("🔧 Creating database tables...")
        db.create_all()
        print("✅ Database tables created successfully!")
        
        # Create admin user if doesn't exist
        admin_email = "admin@example.com"
        admin = User.query.filter_by(email=admin_email).first()
        
        if not admin:
            print(f"\n👤 Creating admin user: {admin_email}")
            admin_user = User(
                email=admin_email,
                phone_number="+1234567890",
                ethereum_address="0x0000000000000000000000000000000000000001",
                role='admin'
            )
            admin_user.set_password("Admin@123")
            db.session.add(admin_user)
            db.session.commit()
            print("✅ Admin user created successfully!")
            print(f"   Email: {admin_email}")
            print(f"   Password: Admin@123")
            print("\n⚠️  IMPORTANT: Change this password after first login!")
        else:
            print(f"\n✅ Admin user already exists: {admin_email}")
        
        print("\n🎉 Database initialization complete!")

if __name__ == "__main__":
    initialize_database()
