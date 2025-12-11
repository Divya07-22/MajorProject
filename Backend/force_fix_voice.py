with open('app.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
skip_count = 0

for i, line in enumerate(lines):
    if skip_count > 0:
        skip_count -= 1
        continue
    
    # Find and replace the admin check block
    if 'claims = get_jwt()' in line and i < len(lines) - 3:
        if 'Admin access required' in lines[i+2]:
            # Replace entire block
            new_lines.append('        current_user_id = get_jwt_identity()\n')
            new_lines.append('        data = request.get_json()\n')
            new_lines.append('        transaction_id = data.get(\'transaction_id\')\n')
            new_lines.append('        \n')
            new_lines.append('        # Get user data\n')
            new_lines.append('        user = User.query.get(current_user_id)\n')
            skip_count = 6  # Skip next 6 lines of old code
            continue
    
    new_lines.append(line)

with open('app.py', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print('✅ Voice call endpoint fixed - removed admin check')
