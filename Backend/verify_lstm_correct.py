with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Correct check
if 'Using stable ensemble' in content:
    print(' LSTM FIXED - Using stable Isolation Forest + XGBoost ensemble')
else:
    print(' LSTM NOT FIXED')
