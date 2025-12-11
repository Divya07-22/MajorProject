with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Check if LSTM is removed OR handled properly
if 'lstm_autoencoder = None' in content or 'LSTM removed' in content:
    print(' LSTM FIXED - Set to None (stable ensemble approach)')
elif 'tf.keras.models.load_model' in content and 'lstm_autoencoder.h5' in content:
    print(' LSTM NOT FIXED - Still loading file')
    # FIX IT NOW
    old = 'lstm_autoencoder = tf.keras.models.load_model('
    new = '# LSTM removed for stability\n    lstm_autoencoder = None\n    # Original: lstm_autoencoder = tf.keras.models.load_model('
    content = content.replace(old, new)
    
    with open('app.py', 'w', encoding='utf-8') as f2:
        f2.write(content)
    print(' FIXED NOW - LSTM removed')
else:
    print(' LSTM code not found - may already be different')
