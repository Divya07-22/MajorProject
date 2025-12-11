with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Remove admin check from voice-call endpoint
old_code = '''    claims = get_jwt()
        if claims.get('role') != 'admin':
            return jsonify({"error": "Admin access required"}), 403

        data = request.get_json()
        user_id = data.get('user_id')
        user = User.query.get(user_id)'''

new_code = '''    current_user_id = get_jwt_identity()
        data = request.get_json()
        transaction_id = data.get('transaction_id')
        
        # Get user's own data
        user = User.query.get(current_user_id)'''

content = content.replace(old_code, new_code)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('✅ Removed admin restriction from voice-call endpoint')
print('✅ Now any authenticated user can initiate calls for their own transactions')
print('\nRestart Flask: Ctrl+C then python app.py')
