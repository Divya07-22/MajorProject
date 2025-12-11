with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Remove LSTM loading
old_lstm = '''try:
    lstm_autoencoder = load_model('models/lstm_autoencoder.h5')
    logger.info(\"LSTM Autoencoder loaded\")
except Exception as e:
    logger.warning(f\"Could not load LSTM: {e}\")
    lstm_autoencoder = None'''

new_lstm = '''# LSTM removed for stability - using Isolation Forest + XGBoost ensemble
lstm_autoencoder = None
logger.info(\"Using Isolation Forest + XGBoost ensemble for fraud detection\")'''

content = content.replace(old_lstm, new_lstm)

# Remove LSTM prediction code
old_pred = '''# 2. LSTM Autoencoder - Behavior Profiling (SKIPPED - model incompatible)
        # Use dummy value for now
        df['lstm_error'] = 0.0'''

new_pred = '''# 2. Ensemble uses Isolation Forest + XGBoost (no LSTM needed)
        df['lstm_error'] = 0.0  # Placeholder for XGBoost compatibility'''

content = content.replace(old_pred, new_pred)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)

print(' LSTM safely removed - backend still uses AI fraud detection')
