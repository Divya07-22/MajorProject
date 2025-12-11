#!/bin/bash
# scripts/train_all_models.sh

echo "🤖 Starting AI Model Training Pipeline..."
echo "========================================"

# Create necessary directories
mkdir -p models/trained_models
mkdir -p data
mkdir -p logs

# Check if dataset exists
if [ ! -f "data/creditcard.csv" ]; then
    echo "❌ ERROR: data/creditcard.csv not found!"
    echo "Please download the dataset from Kaggle and place it in the data/ folder"
    exit 1
fi

echo ""
echo "📊 Step 1/4: Training Isolation Forest Model..."
python models/1_transaction_anomaly.py
if [ $? -ne 0 ]; then
    echo "❌ Isolation Forest training failed!"
    exit 1
fi

echo ""
echo "🧠 Step 2/4: Training LSTM Autoencoder..."
python models/2_behavior_profiling.py
if [ $? -ne 0 ]; then
    echo "❌ LSTM training failed!"
    exit 1
fi

echo ""
echo "🕸️  Step 3/4: Training Graph Neural Network..."
python models/3_gnn_fraud_detection.py
if [ $? -ne 0 ]; then
    echo "❌ GNN training failed!"
    exit 1
fi

echo ""
echo "🎯 Step 4/4: Training Final XGBoost Meta-Model..."
python models/4_final_risk_model.py
if [ $? -ne 0 ]; then
    echo "❌ XGBoost training failed!"
    exit 1
fi

echo ""
echo "✅ All models trained successfully!"
echo "🎉 Training pipeline complete!"
