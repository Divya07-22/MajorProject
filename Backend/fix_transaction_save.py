import re

with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Find and replace the exact pattern
old_code = '''new_log = TransactionLog(
            user_id=user.id,
            risk_score=risk_score,
            tx_hash=tx_hash_hex,
            status=status_message,
            amount=amount
        )'''

new_code = '''new_log = TransactionLog(
            user_id=user.id,
            risk_score=risk_score,
            tx_hash=tx_hash_hex,
            status=status_message,
            amount=amount,
            merchant=transaction_data.get('merchant'),
            location=transaction_data.get('location'),
            transaction_type=transaction_data.get('transaction_type')
        )'''

content = content.replace(old_code, new_code)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)

print(' Fixed TransactionLog creation!')
