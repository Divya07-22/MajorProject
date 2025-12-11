with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix 1: User model doesn't have 'username' - use 'name' instead
content = content.replace("'username': user.username,", "'name': user.name,")

# Fix 2: Ensure timezone is imported at top of file
if 'from datetime import' in content:
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if 'from datetime import datetime' in line and 'timezone' not in line:
            lines[i] = 'from datetime import datetime, timezone'
            break
    content = '\n'.join(lines)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('FIXED:')
print('  - Changed username to name in profile')
print('  - Added timezone import')
