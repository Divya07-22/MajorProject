# models/1_transaction_anomaly.py (Corrected and Complete)

import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler # <-- IMPORTED
import joblib
import os # <-- IMPORTED

print("Starting Model 1: Isolation Forest & Data Preprocessing...")

# 1. Load Data
df = pd.read_csv('data/creditcard.csv')
features = df.drop(['Time', 'Class'], axis=1)

# --- CRITICAL FIX: Create and Save the Scaler ---
# The app.py server needs this file to process live transactions.
# This was the missing step.
print("Creating and saving the data scaler...")
scaler = StandardScaler()
scaler.fit(features) # Fit the scaler on the full training data

save_path = 'models/trained_models'
os.makedirs(save_path, exist_ok=True) # Ensure the directory exists

joblib.dump(scaler, os.path.join(save_path, 'scaler.joblib'))
print(f"Scaler saved to {os.path.join(save_path, 'scaler.joblib')}")
# --- END OF CRITICAL FIX ---

# 2. Build and Train the Isolation Forest Model
print("Training Isolation Forest model...")
iso_forest = IsolationForest(n_estimators=100, contamination=0.00172, random_state=42, n_jobs=-1)
iso_forest.fit(features)
print("Isolation Forest model trained.")

# 3. Predict Anomaly Scores
df['anomaly_score'] = iso_forest.decision_function(features)
print("Anomaly scores calculated.")

# 4. Save the Trained Model
joblib.dump(iso_forest, os.path.join(save_path, 'isolation_forest.joblib'))
print(f"Model saved to {os.path.join(save_path, 'isolation_forest.joblib')}")

# 5. Save the Results for the next script
output_df = df[['Time', 'Amount', 'Class', 'anomaly_score']]
output_df.to_csv('data/1_iforest_results.csv', index=False)

print("Results saved to data/1_iforest_results.csv")
print("Model 1 complete.")