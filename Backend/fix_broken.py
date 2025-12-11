with open('app.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Fix broken print statements around line 536
for i in range(len(lines)):
    if 'print(f"' in lines[i] and '===' in lines[i+1]:
        # Remove broken multi-line f-string
        lines[i] = '        print("=== TRANSACTION ERROR ===")\n'
        if '===' in lines[i+1]:
            lines[i+1] = ''

with open('app.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print('Fixed broken f-string!')
