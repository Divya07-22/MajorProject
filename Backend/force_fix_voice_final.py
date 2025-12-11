with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Force replace in voice-call endpoint
content = content.replace(
    '''data = request.get_json()
        user_id = data.get('user_id')
        user = User.query.get(user_id)''',
    '''data = request.get_json()
        transaction_id = data.get('transaction_id')
        
        if not transaction_id:
            return jsonify({\"error\": \"transaction_id required\"}), 400
        
        user = User.query.get(current_user_id)'''
)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('✅ FIXED: Voice-call endpoint now uses transaction_id!')
print('Restart Flask NOW!')
