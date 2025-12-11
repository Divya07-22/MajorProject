# Update handle_transaction endpoint
import re

with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Find the section where transaction is saved to database
# Look for: new_log = TransactionLog(
pattern = r'(new_log = TransactionLog\(\s+user_id=user\.id,\s+risk_score=risk_score,\s+status=status,\s+amount=amount)'

replacement = r'''new_log = TransactionLog(
                user_id=user.id,
                risk_score=risk_score,
                status=status,
                amount=amount,
                merchant=transaction_data.get('merchant'),
                location=transaction_data.get('location'),
                transaction_type=transaction_data.get('transaction_type')'''

content = re.sub(pattern, replacement, content)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)

print(' Transaction endpoint updated!')
