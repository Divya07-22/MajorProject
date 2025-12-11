with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix 1: Add Profile GET endpoint
if '@app.route(\'/api/profile\', methods=[\'GET\'])' not in content:
    profile_get = '''
@app.route('/api/profile', methods=['GET'])
@jwt_required()
def get_profile():
    \"\"\"Get user profile\"\"\"
    try:
        current_user_id = int(get_jwt_identity())
        user = db.session.get(User, current_user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'phone_number': user.phone_number,
            'address': user.address,
            'ethereum_address': user.ethereum_address,
            'is_frozen': user.is_frozen,
            'created_at': user.created_at.isoformat()
        }), 200
    except Exception as e:
        logger.error(f'Get profile error: {e}')
        return jsonify({'error': 'Failed to get profile'}), 500

@app.route('/api/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    \"\"\"Update user profile\"\"\"
    try:
        current_user_id = int(get_jwt_identity())
        user = db.session.get(User, current_user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        data = request.get_json()
        
        if 'phone_number' in data:
            user.phone_number = data['phone_number']
        if 'address' in data:
            user.address = data['address']
        if 'ethereum_address' in data:
            user.ethereum_address = data['ethereum_address']
        
        db.session.commit()
        
        return jsonify({'message': 'Profile updated successfully'}), 200
    except Exception as e:
        logger.error(f'Update profile error: {e}')
        return jsonify({'error': 'Failed to update profile'}), 500
'''
    # Insert before health check
    content = content.replace('@app.route(\'/api/health\', methods=[\'GET\'])', 
                            profile_get + '\n@app.route(\'/api/health\', methods=[\'GET\'])')

# Fix 2: Remove emojis manually
content = content.replace('\" Connected to MongoDB\"', '\"Connected to MongoDB\"')
content = content.replace('\" Connected to blockchain. Account:', '\"Connected to blockchain. Account:')
content = content.replace('\" Twilio client initialized\"', '\"Twilio client initialized\"')
content = content.replace('\" Isolation Forest loaded\"', '\"Isolation Forest loaded\"')
content = content.replace('\" LSTM Autoencoder loaded\"', '\"LSTM Autoencoder loaded\"')
content = content.replace('\" XGBoost model loaded\"', '\"XGBoost model loaded\"')
content = content.replace('\" Scaler loaded\"', '\"Scaler loaded\"')
content = content.replace('\" All AI models loaded successfully\"', '\"All AI models loaded successfully\"')
content = content.replace('\" FraudMitigator contract loaded\"', '\"FraudMitigator contract loaded\"')
content = content.replace('\" FraudLedger contract loaded\"', '\"FraudLedger contract loaded\"')
content = content.replace('\" Starting Flask application...\"', '\"Starting Flask application...\"')

# Fix 3: Replace User.query.get with db.session.get
content = content.replace('User.query.get(current_user_id)', 'db.session.get(User, current_user_id)')

# Fix 4: Replace datetime.utcnow() with datetime.now(timezone.utc)
if 'from datetime import datetime, timezone' not in content:
    content = content.replace('from datetime import datetime', 'from datetime import datetime, timezone')
content = content.replace('datetime.utcnow()', 'datetime.now(timezone.utc)')

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('FIXED ALL ERRORS!')
print('  - Added /api/profile GET and PUT endpoints')
print('  - Removed emoji characters from logging')
print('  - Fixed SQLAlchemy legacy warnings')
print('  - Fixed datetime deprecation warnings')
