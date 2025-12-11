#!/bin/bash
# zkp/compile_circuit.sh
# Compile ZoKrates circuit

echo "🔐 Compiling ZK Circuit..."

# Check if ZoKrates is installed
if ! command -v zokrates &> /dev/null; then
    echo "❌ ZoKrates is not installed!"
    echo "Install from: https://zokrates.github.io/gettingstarted.html"
    exit 1
fi

# Navigate to zkp directory
cd zkp

# Compile the circuit
echo "Compiling risk_check.zok..."
zokrates compile -i risk_check.zok

if [ $? -eq 0 ]; then
    echo "✅ Circuit compiled successfully!"
    echo "Output: zkp/out"
else
    echo "❌ Compilation failed!"
    exit 1
fi
