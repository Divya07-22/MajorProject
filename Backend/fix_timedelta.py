with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Add timedelta to datetime import
content = content.replace('from datetime import datetime, timezone', 
                         'from datetime import datetime, timezone, timedelta')

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('Added timedelta import!')
