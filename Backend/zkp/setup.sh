#!/bin/bash
# zkp/setup.sh
# Generate proving and verification keys

echo "🔑 Generating ZK Proof Keys..."

cd zkp

# Check if circuit is compiled
if [ ! -f "out" ]; then
    echo "❌ Circuit not compiled! Run compile_circuit.sh first"
    exit 1
fi

# Perform the setup ceremony
echo "Running setup ceremony..."
zokrates setup

if [ $? -eq 0 ]; then
    echo "✅ Proving and verification keys generated!"
    ls -lh proving.key verification.key
else
    echo "❌ Setup failed!"
    exit 1
fi

# Export Solidity verifier
echo ""
echo "Exporting Solidity verifier..."
zokrates export-verifier

if [ $? -eq 0 ]; then
    echo "✅ Verifier contract exported to verifier.sol"
    echo "Copy this to contracts/Verifier.sol"
else
    echo "❌ Export failed!"
    exit 1
fi
