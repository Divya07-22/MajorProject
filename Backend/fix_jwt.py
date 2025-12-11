import re

with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Find: access_token = create_access_token(identity=user.id
# Replace with: access_token = create_access_token(identity=str(user.id)

content = re.sub(
    r'create_access_token\(identity=user\.id',
    'create_access_token(identity=str(user.id)',
    content
)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)

print(' Fixed JWT identity to string!')
