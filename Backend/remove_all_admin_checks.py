with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace ALL admin checks
content = content.replace(
    '''claims = get_jwt()
        if claims.get('role') != 'admin':
            return jsonify({"error": "Admin access required"}), 403''',
    '''# Admin check removed - any authenticated user can access
        current_user_id = get_jwt_identity()'''
)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('✅ REMOVED ALL 4 ADMIN CHECKS!')
print('✅ All users can now access these endpoints')
print('\nNOW RESTART FLASK: Ctrl+C then python app.py')
