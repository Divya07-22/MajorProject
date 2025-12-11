with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix 1: Replace the second (main) twilio call
old = '''public_url = os.environ.get('PUBLIC_URL', 'http://localhost:5000')
        webhook_url = f\"{public_url}/api/voice-response/{user.id}\"

        call = twilio_client.calls.create(
            to=user.phone_number,
            from_=os.environ.get('TWILIO_PHONE_NUMBER'),
            url=webhook_url
        )

        logger.info(f\"Voice call initiated for {user.email}, SID: {call.sid}\")
        return jsonify({\"message\": \"Voice call initiated\", \"call_sid\": call.sid}), 200'''

new = '''public_url = os.environ.get('PUBLIC_URL', 'http://localhost:5000')
        
        # Check if localhost (Twilio doesn't support localhost)
        if 'localhost' in public_url or '127.0.0.1' in public_url:
            logger.info(f\"Voice call simulated for {user.email} (localhost mode)\")
            return jsonify({
                \"message\": \"Voice call endpoint working (simulated)\",
                \"status\": \"success\",
                \"phone_number\": user.phone_number,
                \"transaction_id\": transaction_id,
                \"note\": \"Deploy with public URL for real calls\"
            }), 200
        
        webhook_url = f\"{public_url}/api/voice-response/{user.id}\"

        call = twilio_client.calls.create(
            to=user.phone_number,
            from_=os.environ.get('TWILIO_PHONE_NUMBER'),
            url=webhook_url
        )

        logger.info(f\"Voice call initiated for {user.email}, SID: {call.sid}\")
        return jsonify({\"message\": \"Voice call initiated\", \"call_sid\": call.sid}), 200'''

content = content.replace(old, new)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('✅ Fixed voice-call to handle localhost!')
print('Restart Flask!')
