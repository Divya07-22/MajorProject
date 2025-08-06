# models/1_transaction_anomaly.py

import pandas as pd
from sklearn.ensemble import IsolationForest
import joblib

print("Starting Model 1: Isolation Forest Anomaly Detection...")

# 1. Load Data
df = pd.read_csv('data/creditcard.csv')

# We only need the transaction features (V1-V28, Amount) for this model
features = df.drop(['Time', 'Class'], axis=1)

# 2. Build and Train the Model
# The 'contamination' parameter is an estimate of the proportion of outliers in the data.
# The dataset description says frauds are 0.172% of transactions.
iso_forest = IsolationForest(n_estimators=100, contamination=0.00172, random_state=42, n_jobs=-1)
iso_forest.fit(features)

print("Isolation Forest model trained.")

# 3. Predict Anomaly Scores
# The model returns -1 for anomalies (fraud) and 1 for inliers (normal).
# We also get a decision_function score (lower is more anomalous).
df['anomaly_score'] = iso_forest.decision_function(features)
df['is_anomaly'] = iso_forest.predict(features)

# Convert predictions to a more intuitive 0 (normal) and 1 (anomaly/fraud)
df['is_anomaly'] = df['is_anomaly'].apply(lambda x: 1 if x == -1 else 0)

print("Anomaly scores calculated.")

# 4. Save the Trained Model
joblib.dump(iso_forest, 'models/trained_models/isolation_forest.joblib')
print("Model saved to models/trained_models/isolation_forest.joblib")

# 5. Save the Results
# We will save the original data along with the new anomaly scores.
# This output will be used by our final XGBoost model.
output_df = df[['Time', 'Amount', 'Class', 'anomaly_score', 'is_anomaly']]
output_df.to_csv('data/1_iforest_results.csv', index=False)

print("Results saved to data/1_iforest_results.csv")
print("Model 1 complete.")