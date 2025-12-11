# Update TransactionLog model in app.py
import re

with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Find and replace TransactionLog class
old_model = r'''class TransactionLog\(db\.Model\):
    __tablename__ = 'transaction_log'
    id = db\.Column\(db\.Integer, primary_key=True\)
    user_id = db\.Column\(db\.Integer, db\.ForeignKey\('user\.id'\), nullable=False\)
    timestamp = db\.Column\(db\.DateTime, default=datetime\.utcnow\)
    risk_score = db\.Column\(db\.Float, nullable=False\)
    status = db\.Column\(db\.String\(100\)\)
    tx_hash = db\.Column\(db\.String\(66\), nullable=True\)
    amount = db\.Column\(db\.Float, nullable=True\)'''

new_model = '''class TransactionLog(db.Model):
    __tablename__ = 'transaction_log'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    risk_score = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(100))
    tx_hash = db.Column(db.String(66), nullable=True)
    amount = db.Column(db.Float, nullable=True)
    merchant = db.Column(db.String(255), nullable=True)
    location = db.Column(db.String(255), nullable=True)
    transaction_type = db.Column(db.String(100), nullable=True)'''

content = re.sub(old_model, new_model, content)

# Update to_dict method to include new fields
old_to_dict = r'''def to_dict\(self\):
        return \{
            'id': self\.id,
            'user_id': self\.user_id,
            'timestamp': self\.timestamp\.isoformat\(\),
            'risk_score': self\.risk_score,
            'status': self\.status,
            'tx_hash': self\.tx_hash,
            'amount': self\.amount'''

new_to_dict = '''def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'timestamp': self.timestamp.isoformat(),
            'risk_score': self.risk_score,
            'status': self.status,
            'tx_hash': self.tx_hash,
            'amount': self.amount,
            'merchant': self.merchant,
            'location': self.location,
            'transaction_type': self.transaction_type'''

content = re.sub(old_to_dict, new_to_dict, content)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)

print(' TransactionLog model updated!')
