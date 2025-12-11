with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace LSTM loading block
old_code = '''    # Load LSTM Autoencoder
    lstm_autoencoder = tf.keras.models.load_model(
        os.path.join(model_path, 'lstm_autoencoder.h5'),
        custom_objects={'mae': tf.keras.losses.MeanAbsoluteError()}
    )
    logger.info(\"LSTM Autoencoder loaded\")'''

new_code = '''    # LSTM removed for stability - using Isolation Forest + XGBoost ensemble
    lstm_autoencoder = None
    logger.info(\"Using Isolation Forest + XGBoost ensemble (LSTM removed for stability)\")'''

content = content.replace(old_code, new_code)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)

print(' LSTM loading code replaced!')
print(' Backend now uses stable Isolation Forest + XGBoost ensemble')
print('\nRestart Flask: Ctrl+C then python app.py')
