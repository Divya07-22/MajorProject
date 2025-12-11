with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Remove 'time' line
old = '''    return {
        'time': 172792.0,
        'V1': -1.359807, 'V2': -0.072781, 'V3': 2.536347, 'V4': 1.378155,'''

new = '''    return {
        'V1': -1.359807, 'V2': -0.072781, 'V3': 2.536347, 'V4': 1.378155,'''

content = content.replace(old, new)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('Removed time column!')
