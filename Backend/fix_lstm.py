with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix LSTM input - needs 3D reshape
old = '''# 2. LSTM Autoencoder - Behavior Profiling
        reconstruction = lstm_autoencoder.predict(scaled_features, verbose=0)'''

new = '''# 2. LSTM Autoencoder - Behavior Profiling
        # Reshape for LSTM: (batch, timesteps, features)
        lstm_input = scaled_features.reshape((scaled_features.shape[0], 1, scaled_features.shape[1]))
        reconstruction = lstm_autoencoder.predict(lstm_input, verbose=0)
        reconstruction = reconstruction.reshape((reconstruction.shape[0], -1))'''

content = content.replace(old, new)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('Fixed LSTM reshape!')
