with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace with exact spacing
old = '''access_token = create_access_token(
              identity=user.id,
              additional_claims={'role': user.role}
          )'''

new = '''access_token = create_access_token(
              identity=str(user.id),
              additional_claims={'role': user.role}
          )'''

content = content.replace(old, new)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)

print(' Fixed!')
