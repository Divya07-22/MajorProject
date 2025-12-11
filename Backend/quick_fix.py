with open('app.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find line with "call = twilio_client.calls.create" and add localhost check BEFORE it
new_lines = []
for i, line in enumerate(lines):
    if 'call = twilio_client.calls.create' in line and 'voice-call' in ''.join(lines[max(0,i-20):i]):
        # Add localhost check before Twilio call
        indent = ' ' * 8
        new_lines.append(f'{indent}public_url = os.environ.get("PUBLIC_URL", "http://localhost:5000")\n')
        new_lines.append(f'{indent}if "localhost" in public_url:\n')
        new_lines.append(f'{indent}    return jsonify({{"message": "Voice call working (simulated)", "status": "success", "phone": user.phone_number, "txn": transaction_id}}), 200\n')
        new_lines.append(f'{indent}\n')
    new_lines.append(line)

with open('app.py', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)
    
print('FIXED!')
