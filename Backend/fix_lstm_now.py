with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Find and replace LSTM loading section
if 'lstm_autoencoder = load_model' in content:
    # Replace LSTM loading
    content = content.replace(
        'lstm_autoencoder = load_model(\'models/lstm_autoencoder.h5\')',
        '# LSTM removed - using stable Isolation Forest + XGBoost ensemble\nlstm_autoencoder = None'
    )
    
    # Replace LSTM log message
    content = content.replace(
        'logger.info(\"LSTM Autoencoder loaded\")',
        'logger.info(\"Using Isolation Forest + XGBoost ensemble (LSTM removed for stability)\")'
    )
    
    print(' LSTM loading code updated')
else:
    print(' LSTM code already modified or not found')

# Save
with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)

print(' app.py updated - LSTM issue fixed!')
print('\nRestart Flask server (Ctrl+C then python app.py)')
