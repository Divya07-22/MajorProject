import re

# Read app.py
with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# New health check function
new_function = '''def health_check():
    """System health check endpoint"""
    from sqlalchemy import text
    from datetime import datetime, timezone
    
    db_status = False
    try:
        db.session.execute(text('SELECT 1'))
        db.session.commit()
        db_status = True
    except Exception as e:
        logger.error(f"Database health check failed: {e}")

    blockchain_status = False
    try:
        blockchain_status = w3.is_connected() if w3 else False
    except Exception as e:
        logger.error(f"Blockchain health check failed: {e}")

    mongo_status = False
    try:
        mongo_client.admin.command('ping')
        mongo_status = True
    except Exception as e:
        logger.error(f"MongoDB health check failed: {e}")

    overall_status = db_status and blockchain_status and mongo_status

    return jsonify({
        'status': 'healthy' if overall_status else 'degraded',
        'services': {
            'database': db_status,
            'blockchain': blockchain_status,
            'mongodb': mongo_status
        },
        'timestamp': datetime.now(timezone.utc).isoformat()
    }), 200 if overall_status else 503'''

# Replace old function
pattern = r'def health_check\(\):.*?(?=\n@app\.route|\ndef \w+\()'
content = re.sub(pattern, new_function, content, flags=re.DOTALL)

# Write back
with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)

print(' Health check fixed!')
