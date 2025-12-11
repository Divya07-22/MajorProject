# utils/blockchain_helper.py
import time
import logging
from web3.exceptions import TransactionNotFound, BlockNotFound

logger = logging.getLogger(__name__)

def retry_transaction(transaction_func, max_retries=3, backoff_factor=2):
    """
    Retry blockchain transactions with exponential backoff
    
    Args:
        transaction_func: Function that executes the transaction
        max_retries: Maximum number of retry attempts
        backoff_factor: Multiplier for wait time between retries
    
    Returns:
        Result of the transaction function
    """
    for attempt in range(max_retries):
        try:
            result = transaction_func()
            logger.info(f"Transaction successful on attempt {attempt + 1}")
            return result
        except Exception as e:
            if attempt == max_retries - 1:
                logger.error(f"Transaction failed after {max_retries} attempts: {e}")
                raise e
            
            wait_time = backoff_factor ** attempt
            logger.warning(
                f"Transaction failed (attempt {attempt + 1}/{max_retries}). "
                f"Retrying in {wait_time}s... Error: {str(e)}"
            )
            time.sleep(wait_time)

def wait_for_transaction_receipt(web3, tx_hash, timeout=120):
    """
    Wait for transaction receipt with timeout
    
    Args:
        web3: Web3 instance
        tx_hash: Transaction hash
        timeout: Maximum time to wait in seconds
    
    Returns:
        Transaction receipt
    """
    start_time = time.time()
    
    while time.time() - start_time < timeout:
        try:
            receipt = web3.eth.get_transaction_receipt(tx_hash)
            if receipt is not None:
                logger.info(f"Transaction receipt received: {tx_hash}")
                return receipt
        except TransactionNotFound:
            pass
        
        time.sleep(2)
    
    raise TimeoutError(f"Transaction receipt not found within {timeout} seconds")

def estimate_gas_with_buffer(web3, transaction, buffer_percentage=20):
    """
    Estimate gas for transaction with buffer
    
    Args:
        web3: Web3 instance
        transaction: Transaction dictionary
        buffer_percentage: Percentage to add as buffer
    
    Returns:
        Estimated gas with buffer
    """
    estimated_gas = web3.eth.estimate_gas(transaction)
    buffered_gas = int(estimated_gas * (1 + buffer_percentage / 100))
    logger.info(f"Gas estimate: {estimated_gas}, with buffer: {buffered_gas}")
    return buffered_gas
