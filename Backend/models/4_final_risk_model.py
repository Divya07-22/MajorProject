# models/4_final_risk_model.py

import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
import os

print("Starting Final Model: Updating XGBoost Meta-Model with all expert scores...")

# --- 1. Load All Data Sources ---
base_df = pd.read_csv('data/creditcard.csv')
iforest_df = pd.read_csv('data/1_iforest_results.csv')
lstm_df = pd.read_csv('data/2_lstm_results.csv')
gnn_df = pd.read_csv('data/3_gnn_results.csv')

# --- 2. Combine into a Single, Powerful Feature Set ---
final_df = base_df.copy()
final_df['anomaly_score'] = iforest_df['anomaly_score']
final_df['lstm_error'] = lstm_df['lstm_error']
final_df['gnn_pred'] = gnn_df['gnn_pred']

final_df['lstm_error'].fillna(0, inplace=True) 
final_df['gnn_pred'].replace(-1, final_df['gnn_pred'].mode()[0], inplace=True)

print("Feature set created by combining outputs from Isolation Forest, LSTM, and GNN.")

# --- 3. Prepare Data for XGBoost ---
X = final_df.drop(['Class'], axis=1)
y = final_df['Class']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# --- 4. Train the Final XGBoost Classifier ---
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
save_path = 'models/trained_models'
os.makedirs(save_path, exist_ok=True)
xgb_clf.save_model(os.path.join(save_path, 'xgb_risk_model.json'))
print(f"Final, enhanced risk model saved to {os.path.join(save_path, 'xgb_risk_model.json')}")
print("AI Engine phase is now complete.")