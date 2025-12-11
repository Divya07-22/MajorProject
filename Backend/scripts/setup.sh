#!/bin/bash
# scripts/setup.sh - Complete Backend Setup Script

echo "🚀 Starting Backend Setup..."
echo "=============================="

# Check Python version
python_version=$(python --version 2>&1 | awk '{print $2}')
echo "✓ Python version: $python_version"

# Create directories
echo ""
echo "📁 Creating directories..."
mkdir -p logs keys models/trained_models data utils scripts tests zkp/out
touch logs/.gitkeep keys/.gitkeep

# Install dependencies
echo ""
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

# Validate environment
echo ""
echo "🔍 Validating environment variables..."
python scripts/validate_env.py

# Start databases
echo ""
echo "🗄️  Starting PostgreSQL and MongoDB..."
docker-compose up -d

# Wait for databases
echo "⏳ Waiting for databases to be ready..."
sleep 10

# Initialize database
echo ""
echo "💾 Initializing database..."
python scripts/init_db.py

# Deploy smart contracts
echo ""
echo "📜 Deploying smart contracts..."
truffle migrate --reset

echo ""
echo "⚠️  IMPORTANT: Update .env with new contract addresses!"
echo ""

# Train models (optional - requires dataset)
read -p "Do you want to train AI models now? (requires creditcard.csv) [y/N]: " train_models
if [[ $train_models =~ ^[Yy]$ ]]; then
    bash scripts/train_all_models.sh
fi

echo ""
echo "✅ Backend setup complete!"
echo ""
echo "🎯 Next steps:"
echo "1. Update .env with deployed contract addresses"
echo "2. Run: python app.py (development)"
echo "   OR: gunicorn -c gunicorn_config.py app:app (production)"
echo ""
echo "🌐 API will be available at: http://localhost:5000"
echo "📊 Health check: http://localhost:5000/api/health"
