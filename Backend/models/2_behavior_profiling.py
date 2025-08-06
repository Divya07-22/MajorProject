# models/2_behavior_profiling.py

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, LSTM, RepeatVector
import tensorflow as tf

print("Starting Model 2: LSTM Autoencoder for Behavior Profiling...")
tf.random.set_seed(42) # for reproducibility

# 1. Load Data
df = pd.read_csv('data/creditcard.csv')

# Preprocessing: Scale 'Amount' and 'Time'
scaler = StandardScaler()
df['scaled_amount'] = scaler.fit_transform(df['Amount'].values.reshape(-1, 1))
df['scaled_time'] = scaler.fit_transform(df['Time'].values.reshape(-1, 1))
df_scaled = df.drop(['Time', 'Amount'], axis=1)

# We will train the autoencoder only on normal transactions
normal_df = df_scaled[df_scaled['Class'] == 0].drop('Class', axis=1)
fraud_df = df_scaled[df_scaled['Class'] == 1].drop('Class', axis=1)

# 2. Create Sequences
# We create sequences of transactions to model user behavior over time.
def create_sequences(X, time_steps=10):
    Xs = []
    for i in range(len(X) - time_steps):
        Xs.append(X.iloc[i:(i + time_steps)].values)
    return np.array(Xs)

TIME_STEPS = 10
X_train = create_sequences(normal_df, TIME_STEPS)
print(f"Training data shape: {X_train.shape}")

# 3. Build the LSTM Autoencoder Model
n_features = X_train.shape[2]

# Encoder
input_layer = Input(shape=(TIME_STEPS, n_features))
encoder = LSTM(128, activation='relu', input_shape=(TIME_STEPS, n_features), return_sequences=False)(input_layer)
encoder = RepeatVector(TIME_STEPS)(encoder)

# Decoder
decoder = LSTM(128, activation='relu', return_sequences=True)(encoder)
output_layer = tf.keras.layers.TimeDistributed(tf.keras.layers.Dense(n_features))(decoder)

# Autoencoder
lstm_autoencoder = Model(inputs=input_layer, outputs=output_layer)
lstm_autoencoder.compile(optimizer='adam', loss='mae')
lstm_autoencoder.summary()

# 4. Train the Model
history = lstm_autoencoder.fit(X_train, X_train, epochs=10, batch_size=32, validation_split=0.1, shuffle=False)
print("LSTM Autoencoder model trained.")

# 5. Calculate Reconstruction Error
# We create sequences for the entire dataset to test the model
full_sequences = create_sequences(df_scaled.drop('Class', axis=1), TIME_STEPS)
reconstructions = lstm_autoencoder.predict(full_sequences)
mse = np.mean(np.power(full_sequences - reconstructions, 2), axis=(1, 2))

# The results (mse) will be shorter than the original dataframe by TIME_STEPS.
# We'll create a dataframe for these scores.
results_df = pd.DataFrame()
results_df['lstm_error'] = mse
# Add a buffer of NaNs at the beginning to align with original dataframe if needed later
padding = pd.DataFrame([np.nan] * TIME_STEPS, columns=['lstm_error'])
results_df = pd.concat([padding, results_df], ignore_index=True)


print("Reconstruction error calculated for all transactions.")

# 6. Save the Trained Model and Results
lstm_autoencoder.save('models/trained_models/lstm_autoencoder.h5')
print("Model saved to models/trained_models/lstm_autoencoder.h5")

results_df.to_csv('data/2_lstm_results.csv', index=False)
print("Results saved to data/2_lstm_results.csv")
print("Model 2 complete.")