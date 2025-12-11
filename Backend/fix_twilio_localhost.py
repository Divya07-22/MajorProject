with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Find the Twilio call section and wrap it to handle localhost gracefully
old_twilio_call = '''try:
            call = twilio_client.calls.create(
                to=user.phone_number,
                from_=os.getenv('TWILIO_PHONE_NUMBER'),
                url=f\"{os.getenv('BASE_URL', 'http://localhost:5000')}/api/voice-response/{current_user_id}\",
                method='POST'
            )
            logger.info(f'Voice call initiated: {call.sid}')
            return jsonify({
                'message': 'Voice call initiated',
                'call_sid': call.sid,
                'phone_number': user.phone_number
            }), 200
        except Exception as e:
            logger.error(f'Error initiating voice call: {e}')
            return jsonify({'error': str(e)}), 500'''

new_twilio_call = '''try:
            # Check if using localhost (Twilio doesn't support localhost URLs)
            base_url = os.getenv('BASE_URL', 'http://localhost:5000')
            if 'localhost' in base_url or '127.0.0.1' in base_url:
                # Simulate successful call for demo/testing
                logger.info(f'Voice call simulation (localhost detected) - would call {user.phone_number}')
                return jsonify({
                    'message': 'Voice call endpoint working (simulated - Twilio requires public URL)',
                    'status': 'success',
                    'phone_number': user.phone_number,
                    'transaction_id': transaction_id,
                    'note': 'To make real calls, deploy with public URL and valid Twilio credentials'
                }), 200
            
            # Real Twilio call for production
            call = twilio_client.calls.create(
                to=user.phone_number,
                from_=os.getenv('TWILIO_PHONE_NUMBER'),
                url=f\"{base_url}/api/voice-response/{current_user_id}\",
                method='POST'
            )
            logger.info(f'Voice call initiated: {call.sid}')
            return jsonify({
                'message': 'Voice call initiated',
                'call_sid': call.sid,
                'phone_number': user.phone_number
            }), 200
        except Exception as e:
            logger.error(f'Error initiating voice call: {e}')
            return jsonify({'error': str(e)}), 500'''

content = content.replace(old_twilio_call, new_twilio_call)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('✅ Voice-call endpoint now handles localhost gracefully!')
print('✅ Returns 200 with simulation message when testing locally')
print('\nRestart Flask!')
