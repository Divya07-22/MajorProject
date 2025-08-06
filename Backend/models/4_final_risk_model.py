# models/4_final_risk_model.py

import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
import joblib

print("Starting Final Model: Updating XGBoost Meta-Model with all expert scores...")

# --- 1. Load All Data Sources ---
# Original data
base_df = pd.read_csv('data/creditcard.csv')
# Results from Model 1 (Isolation Forest)
iforest_df = pd.read_csv('data/1_iforest_results.csv')
# Results from Model 2 (LSTM)
lstm_df = pd.read_csv('data/2_lstm_results.csv')
# Results from Model 3 (GNN)
gnn_df = pd.read_csv('data/3_gnn_results.csv')

# --- 2. Combine into a Single, Powerful Feature Set ---
# Create the final dataframe by merging all expert model scores
final_df = base_df.copy()
final_df['anomaly_score'] = iforest_df['anomaly_score']
final_df['lstm_error'] = lstm_df['lstm_error']
final_df['gnn_pred'] = gnn_df['gnn_pred']

# Handle missing values from the models
# LSTM errors were padded with NaNs
final_df['lstm_error'].fillna(0, inplace=True) 
# GNN predictions were padded with -1 for transactions not in the sample
final_df['gnn_pred'].replace(-1, final_df['gnn_pred'].mode()[0], inplace=True) # Replace padding with the mode

print("Feature set created by combining outputs from Isolation Forest, LSTM, and GNN.")

# --- 3. Prepare Data for XGBoost ---
# X includes original features PLUS the new expert model scores
X = final_df.drop(['Class'], axis=1)
# y is the ground truth (what actually happened)
y = final_df['Class']

# Split data for training and testing
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# --- 4. Train the Final XGBoost Classifier ---
# The scale_pos_weight is crucial for imbalanced datasets
scale_pos_weight = y_train.value_counts()[0] / y_train.value_counts()[1]

xgb_clf = xgb.XGBClassifier(
    objective='binary:logistic',
    scale_pos_weight=scale_pos_weight,
    use_label_encoder=False,
    eval_metric='logloss',
    n_estimators=200,
    learning_rate=0.1,
    max_depth=5,
    random_state=42,
    n_jobs=-1
)

xgb_clf.fit(X_train, y_train)
print("Final XGBoost meta-model trained.")

# --- 5. Evaluate the Final Model ---
y_pred = xgb_clf.predict(X_test)
print("\n--- Final XGBoost Model Evaluation ---")
print(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")
print("\nClassification Report:")
print(classification_report(y_test, y_pred, target_names=['Normal', 'Fraud']))
print("--------------------------------------\n")

# --- 6. Save the Final, Most Powerful Model ---
xgb_clf.save_model('models/trained_models/xgb_risk_model.json')
print("Final, enhanced risk model saved to models/trained_models/xgb_risk_model.json")
print("AI Engine phase is now complete.")