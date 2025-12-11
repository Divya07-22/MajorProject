with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix scaler - exclude Time
old = '''# 1. Isolation Forest - Anomaly Detection
        scaled_features = scaler.transform(df[required_cols])'''

new = '''# 1. Isolation Forest - Anomaly Detection
        # Scaler only works on V1-V28 + Amount (29 features)
        scaler_cols = [c for c in required_cols if c != 'Time']
        scaled_features = scaler.transform(df[scaler_cols])'''

content = content.replace(old, new)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('Fixed scaler!')
