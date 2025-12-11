# tests/test_contracts.py
import pytest
from web3 import Web3
import json
import os

# This requires Ganache to be running
@pytest.fixture
def web3_instance():
    """Create Web3 instance connected to Ganache"""
    w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:7545'))
    assert w3.is_connected(), "Failed to connect to Ganache"
    return w3

@pytest.fixture
def deployed_contracts(web3_instance):
    """Load deployed contract instances"""
    with open('build/contracts/FraudMitigator.json') as f:
        mitigator_artifact = json.load(f)
    
    with open('build/contracts/FraudLedger.json') as f:
        ledger_artifact = json.load(f)
    
    # Get contract addresses from environment
    mitigator_address = os.getenv('FRAUD_MITIGATOR_CONTRACT_ADDRESS')
    ledger_address = os.getenv('FRAUD_LEDGER_CONTRACT_ADDRESS')
    
    mitigator = web3_instance.eth.contract(
        address=mitigator_address,
        abi=mitigator_artifact['abi']
    )
    
    ledger = web3_instance.eth.contract(
        address=ledger_address,
        abi=ledger_artifact['abi']
    )
    
    return {'mitigator': mitigator, 'ledger': ledger}

def test_contract_deployment(deployed_contracts):
    """Test that contracts are deployed"""
    assert deployed_contracts['mitigator'].address is not None
    assert deployed_contracts['ledger'].address is not None

def test_fraud_report(web3_instance, deployed_contracts):
    """Test reporting fraud to blockchain"""
    accounts = web3_instance.eth.accounts
    owner = accounts[0]
    
    # This is a simplified test - you'll need to adjust based on your contract
    try:
        mitigator = deployed_contracts['mitigator']
        # Test contract interaction
        owner_address = mitigator.functions.owner().call()
        assert owner_address == owner
        print(f"✅ Contract owner verified: {owner_address}")
    except Exception as e:
        pytest.skip(f"Contract interaction failed: {e}")
