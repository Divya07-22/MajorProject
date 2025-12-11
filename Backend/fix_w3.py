# Fix w3 -> web3 in health check
with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace w3 with web3 in health check
content = content.replace('w3.is_connected()', 'web3.is_connected()')
content = content.replace('if w3 else', 'if web3 else')

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)

print(' Fixed!')
