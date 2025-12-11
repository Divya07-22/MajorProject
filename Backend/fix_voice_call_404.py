with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Find and fix the voice-call endpoint
old_code = '''# Admin check removed - any authenticated user can access
        current_user_id = get_jwt_identity()

        data = request.get_json()
        user_id = data.get('user_id')
        user = User.query.get(user_id)

        if not user:
            return jsonify({\"error\": \"User not found\"}), 404'''

new_code = '''# Admin check removed - any authenticated user can access
        current_user_id = get_jwt_identity()

        data = request.get_json()
        transaction_id = data.get('transaction_id')
        
        if not transaction_id:
            return jsonify({\"error\": \"transaction_id required\"}), 400
        
        # Get user from current session
        user = User.query.get(current_user_id)

        if not user:
            return jsonify({\"error\": \"User not found\"}), 404'''

content = content.replace(old_code, new_code)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('✅ Fixed voice-call endpoint - now uses transaction_id instead of user_id')
print('\nRestart Flask: Ctrl+C then python app.py')
