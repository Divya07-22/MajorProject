from web3 import Web3
import os
import json
import logging

logger = logging.getLogger(__name__)

# Polygon Mumbai Testnet (Free Test Network)
POLYGON_RPC = os.getenv('POLYGON_RPC_URL', 'https://rpc-mumbai.maticvigil.com/')
POLYGON_CHAIN_ID = 80001

class PolygonLayer2:
    def __init__(self, contract_address, contract_abi, private_key):
        try:
            self.web3 = Web3(Web3.HTTPProvider(POLYGON_RPC))
            self.chain_id = POLYGON_CHAIN_ID
            
            if not self.web3.is_connected():
                raise Exception("Cannot connect to Polygon network")
            
            self.account = self.web3.eth.account.from_key(private_key)
            
            self.contract = self.web3.eth.contract(
                address=Web3.to_checksum_address(contract_address),
                abi=contract_abi
            )
            
            balance = self.web3.eth.get_balance(self.account.address)
            balance_matic = self.web3.from_wei(balance, 'ether')
            
            logger.info(f"[OK] Polygon Layer-2 initialized")
            logger.info(f"     Network: Mumbai Testnet")
            logger.info(f"     Account: {self.account.address}")
            logger.info(f"     Balance: {balance_matic} MATIC")
            
            self.enabled = True
            
        except Exception as e:
            logger.warning(f"[WARNING] Polygon L2 not available: {e}")
            self.enabled = False
    
    def is_enabled(self):
        return self.enabled
    
    def log_fraud_to_layer2(self, user_address, risk_score, description):
        if not self.enabled:
            return {'success': False, 'error': 'Polygon not enabled'}
        
        try:
            nonce = self.web3.eth.get_transaction_count(self.account.address)
            
            tx = self.contract.functions.reportSuspiciousActivity(
                Web3.to_checksum_address(user_address),
                int(risk_score * 100),
                description[:100]
            ).build_transaction({
                'chainId': self.chain_id,
                'gas': 200000,
                'gasPrice': self.web3.to_wei('30', 'gwei'),
                'nonce': nonce,
            })
            
            signed_tx = self.web3.eth.account.sign_transaction(tx, self.account.key)
            tx_hash = self.web3.eth.send_raw_transaction(signed_tx.rawTransaction)
            receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash, timeout=10)
            
            logger.info(f"✅ Fraud logged to Polygon Layer-2")
            logger.info(f"   TX Hash: {tx_hash.hex()}")
            logger.info(f"   Block: {receipt['blockNumber']}")
            
            return {
                'success': True,
                'tx_hash': tx_hash.hex(),
                'block_number': receipt['blockNumber'],
                'gas_used': receipt['gasUsed'],
                'network': 'Polygon Mumbai',
                'explorer_url': f"https://mumbai.polygonscan.com/tx/{tx_hash.hex()}"
            }
            
        except Exception as e:
            logger.error(f"❌ Polygon transaction failed: {e}")
            return {'success': False, 'error': str(e)}
    
    def get_transaction_history(self, limit=10):
        try:
            latest_block = self.web3.eth.block_number
            fraud_filter = self.contract.events.FraudReported.create_filter(
                fromBlock=max(0, latest_block - 1000),
                toBlock='latest'
            )
            
            events = fraud_filter.get_all_entries()
            
            return [
                {
                    'tx_hash': event['transactionHash'].hex(),
                    'block': event['blockNumber'],
                    'user': event['args'].get('user'),
                    'risk_score': event['args'].get('riskScore', 0) / 100,
                    'timestamp': event['args'].get('timestamp')
                }
                for event in events[-limit:]
            ]
            
        except Exception as e:
            logger.error(f"Error fetching history: {e}")
            return []
    
    def get_cost_comparison(self):
        eth_gas_price_gwei = 50
        polygon_gas_price_gwei = 30
        gas_used = 200000
        eth_price_usd = 2000
        matic_price_usd = 0.8
        
        eth_cost_usd = (gas_used * eth_gas_price_gwei * 0.000000001 * eth_price_usd)
        polygon_cost_usd = (gas_used * polygon_gas_price_gwei * 0.000000001 * matic_price_usd)
        
        return {
            'ethereum_mainnet': {
                'gas_used': gas_used,
                'gas_price_gwei': eth_gas_price_gwei,
                'cost_usd': round(eth_cost_usd, 4)
            },
            'polygon_layer2': {
                'gas_used': gas_used,
                'gas_price_gwei': polygon_gas_price_gwei,
                'cost_usd': round(polygon_cost_usd, 6)
            },
            'savings': {
                'cost_reduction_usd': round(eth_cost_usd - polygon_cost_usd, 4),
                'percentage_saved': round((1 - polygon_cost_usd / eth_cost_usd) * 100, 2)
            }
        }
