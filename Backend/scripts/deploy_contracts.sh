#!/bin/bash
# scripts/deploy_contracts.sh
# Automated smart contract deployment script

echo "🚀 Starting Smart Contract Deployment..."
echo "========================================"

# Check if Ganache is running
echo ""
echo "🔍 Checking if blockchain is running..."
if ! curl -s http://127.0.0.1:7545 > /dev/null; then
    echo "❌ ERROR: Ganache is not running!"
    echo "Please start Ganache and try again."
    exit 1
fi
echo "✅ Blockchain is running"

# Check if truffle is installed
echo ""
echo "🔍 Checking Truffle installation..."
if ! command -v truffle &> /dev/null; then
    echo "❌ ERROR: Truffle is not installed!"
    echo "Install with: npm install -g truffle"
    exit 1
fi
echo "✅ Truffle is installed"

# Compile contracts
echo ""
echo "📝 Compiling smart contracts..."
truffle compile
if [ $? -ne 0 ]; then
    echo "❌ Compilation failed!"
    exit 1
fi
echo "✅ Contracts compiled successfully"

# Deploy contracts
echo ""
echo "🚢 Deploying contracts to blockchain..."
truffle migrate --reset
if [ $? -ne 0 ]; then
    echo "❌ Deployment failed!"
    exit 1
fi

echo ""
echo "✅ Smart contracts deployed successfully!"
echo ""
echo "⚠️  IMPORTANT: Update your .env file with the new contract addresses!"
echo "Copy the addresses from the output above and paste into .env"
echo ""
echo "Contract addresses to update:"
echo "- FRAUD_MITIGATOR_CONTRACT_ADDRESS"
echo "- FRAUD_LEDGER_CONTRACT_ADDRESS"
