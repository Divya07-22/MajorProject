with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Direct string replacement
content = content.replace(
    'access_token = create_access_token(\n              identity=user.id,',
    'access_token = create_access_token(\n              identity=str(user.id),'
)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)

print(' JWT fixed!')
