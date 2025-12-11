with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Find the isolation forest prediction line and add feature names
old_code = '''# 1. Isolation Forest - Anomaly Detection
        # Scaler only works on V1-V28 + Amount (29 features)
        scaler_cols = [c for c in required_cols if c != 'Time']
        scaled_features = scaler.transform(df[scaler_cols])
        anomaly_pred = isolation_forest.predict(scaled_features)'''

new_code = '''# 1. Isolation Forest - Anomaly Detection
        # Scaler only works on V1-V28 + Amount (29 features)
        scaler_cols = [c for c in required_cols if c != 'Time']
        scaled_features = scaler.transform(df[scaler_cols])
        
        # Create DataFrame with proper column names to avoid warning
        import pandas as pd
        scaled_df = pd.DataFrame(scaled_features, columns=scaler_cols)
        anomaly_pred = isolation_forest.predict(scaled_df)'''

content = content.replace(old_code, new_code)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('FIXED sklearn warning!')
