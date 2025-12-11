# scripts/check_models.py
import os
import sys

MODEL_PATH = 'models/trained_models/'

REQUIRED_FILES = [
    'isolation_forest.joblib',
    'lstm_autoencoder.h5',
    'gnn_model.pth',
    'xgb_risk_model.json',
    'scaler.joblib'
]

def check_models():
    """Verify all trained models exist"""
    print("🔍 Checking for trained AI models...\n")
    
    missing_files = []
    existing_files = []
    
    for file in REQUIRED_FILES:
        file_path = os.path.join(MODEL_PATH, file)
        if os.path.exists(file_path):
            file_size = os.path.getsize(file_path) / (1024 * 1024)  # Convert to MB
            print(f"✅ {file} ({file_size:.2f} MB)")
            existing_files.append(file)
        else:
            print(f"❌ {file} - NOT FOUND")
            missing_files.append(file)
    
    print("\n" + "="*50)
    print(f"Summary: {len(existing_files)}/{len(REQUIRED_FILES)} models found")
    print("="*50)
    
    if missing_files:
        print("\n⚠️  WARNING: Missing model files:")
        for file in missing_files:
            print(f"  - {file}")
        print("\n💡 To train missing models, run:")
        print("   bash scripts/train_all_models.sh")
        sys.exit(1)
    else:
        print("\n🎉 All AI models are present and ready!")
        print("You can now run: python app.py")

if __name__ == "__main__":
    check_models()
