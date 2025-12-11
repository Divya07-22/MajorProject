with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Remove 'name': user.name from profile response
old_profile = '''return jsonify({
            'id': user.id,
            'name': user.name,
            'email': user.email,
            'phone_number': user.phone_number,
            'address': user.address,
            'ethereum_address': user.ethereum_address,
            'is_frozen': user.is_frozen,
            'created_at': user.created_at.isoformat()
        }), 200'''

new_profile = '''return jsonify({
            'id': user.id,
            'email': user.email,
            'phone_number': user.phone_number,
            'ethereum_address': user.ethereum_address,
            'is_frozen': user.is_frozen,
            'role': user.role,
            'created_at': user.created_at.isoformat()
        }), 200'''

content = content.replace(old_profile, new_profile)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('FIXED: Removed name field from profile!')
