import re

with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Find: current_user_id = get_jwt_identity()
# Replace with: current_user_id = int(get_jwt_identity())

content = re.sub(
    r'current_user_id = get_jwt_identity\(\)',
    'current_user_id = int(get_jwt_identity())',
    content
)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)

print(' Fixed JWT identity parsing!')
