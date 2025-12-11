import joblib
scaler = joblib.load('models/trained_models/scaler.joblib')
print("Expected columns:")
print(list(scaler.feature_names_in_))
