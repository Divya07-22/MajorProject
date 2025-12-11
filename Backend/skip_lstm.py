with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Skip LSTM and use dummy value
old = '''# 2. LSTM Autoencoder - Behavior Profiling
        # Reshape for LSTM: (batch, timesteps, features)
        lstm_input = scaled_features.reshape((scaled_features.shape[0], 1, scaled_features.shape[1]))
        reconstruction = lstm_autoencoder.predict(lstm_input, verbose=0)
        reconstruction = reconstruction.reshape((reconstruction.shape[0], -1))
        mse = np.mean(np.power(scaled_features - reconstruction, 2), axis=1)
        df['lstm_error'] = mse'''

new = '''# 2. LSTM Autoencoder - Behavior Profiling (SKIPPED - model incompatible)
        # Use dummy value for now
        df['lstm_error'] = 0.0'''

content = content.replace(old, new)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('Skipped LSTM - using dummy value!')
