# scripts/train_all_models.ps1
Write-Host "Starting AI Model Training Pipeline..." -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if dataset exists
if (!(Test-Path "data\creditcard.csv")) {
    Write-Host "ERROR: data/creditcard.csv not found!" -ForegroundColor Red
    Write-Host "Please download the dataset from Kaggle" -ForegroundColor Yellow
    exit 1
}

Write-Host "Step 1/4: Training Isolation Forest Model..." -ForegroundColor Green
python models/1_transaction_anomaly.py
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Model 1 training failed!" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Step 2/4: Training LSTM Autoencoder..." -ForegroundColor Green
python models/2_behavior_profiling.py
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Model 2 training failed!" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Step 3/4: Training Graph Neural Network..." -ForegroundColor Green
python models/3_gnn_fraud_detection.py
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Model 3 training failed!" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Step 4/4: Training Final XGBoost Meta-Model..." -ForegroundColor Green
python models/4_final_risk_model.py
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Model 4 training failed!" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "All models trained successfully!" -ForegroundColor Green
Write-Host "Training pipeline complete!" -ForegroundColor Cyan
