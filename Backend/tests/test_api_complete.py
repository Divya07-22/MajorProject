# tests/test_api_complete.py
import pytest
import json
from app import app, db, User

@pytest.fixture
def client():
    """Create test client"""
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()

def test_health_check(client):
    """Test health check endpoint"""
    response = client.get('/api/health')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'status' in data

def test_user_registration(client):
    """Test user registration"""
    user_data = {
        'email': 'test@example.com',
        'password': 'Password123',
        'phone_number': '+1234567890',
        'address': '0x71C7656EC7ab88b098defB751B7401B5f6d8976F'
    }
    
    response = client.post('/api/register', 
                          data=json.dumps(user_data),
                          content_type='application/json')
    
    assert response.status_code == 201
    data = json.loads(response.data)
    assert 'message' in data

def test_user_login(client):
    """Test user login"""
    # First register
    user_data = {
        'email': 'test@example.com',
        'password': 'Password123',
        'phone_number': '+1234567890',
        'address': '0x71C7656EC7ab88b098defB751B7401B5f6d8976F'
    }
    client.post('/api/register', 
               data=json.dumps(user_data),
               content_type='application/json')
    
    # Then login
    login_data = {
        'email': 'test@example.com',
        'password': 'Password123'
    }
    
    response = client.post('/api/login',
                          data=json.dumps(login_data),
                          content_type='application/json')
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'access_token' in data

def test_invalid_login(client):
    """Test invalid login credentials"""
    login_data = {
        'email': 'nonexistent@example.com',
        'password': 'WrongPassword'
    }
    
    response = client.post('/api/login',
                          data=json.dumps(login_data),
                          content_type='application/json')
    
    assert response.status_code == 401
