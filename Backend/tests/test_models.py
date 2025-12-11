# tests/test_models.py
import pytest
import os
import joblib
import tensorflow as tf
import xgboost as xgb

MODEL_PATH = 'models/trained_models/'

def test_isolation_forest_exists():
    """Test that Isolation Forest model exists"""
    model_file = os.path.join(MODEL_PATH, 'isolation_forest.joblib')
    assert os.path.exists(model_file), "Isolation Forest model not found"

def test_isolation_forest_loads():
    """Test that Isolation Forest model can be loaded"""
    model_file = os.path.join(MODEL_PATH, 'isolation_forest.joblib')
    if os.path.exists(model_file):
        model = joblib.load(model_file)
        assert model is not None
        print("✅ Isolation Forest loaded successfully")

def test_lstm_model_exists():
    """Test that LSTM model exists"""
    model_file = os.path.join(MODEL_PATH, 'lstm_autoencoder.h5')
    assert os.path.exists(model_file), "LSTM model not found"

def test_lstm_model_loads():
    """Test that LSTM model can be loaded"""
    model_file = os.path.join(MODEL_PATH, 'lstm_autoencoder.h5')
    if os.path.exists(model_file):
        model = tf.keras.models.load_model(model_file)
        assert model is not None
        print("✅ LSTM model loaded successfully")

def test_xgboost_model_exists():
    """Test that XGBoost model exists"""
    model_file = os.path.join(MODEL_PATH, 'xgb_risk_model.json')
    assert os.path.exists(model_file), "XGBoost model not found"

def test_xgboost_model_loads():
    """Test that XGBoost model can be loaded"""
    model_file = os.path.join(MODEL_PATH, 'xgb_risk_model.json')
    if os.path.exists(model_file):
        model = xgb.XGBClassifier()
        model.load_model(model_file)
        assert model is not None
        print("✅ XGBoost model loaded successfully")

def test_scaler_exists():
    """Test that scaler exists"""
    scaler_file = os.path.join(MODEL_PATH, 'scaler.joblib')
    assert os.path.exists(scaler_file), "Scaler not found"
