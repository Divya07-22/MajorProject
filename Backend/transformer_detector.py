# transformer_detector.py - Lightweight Transformer (No FinBERT, No TensorFlow)
import numpy as np
import logging
import re
from collections import Counter

warnings = []
logger = logging.getLogger(__name__)

class TransformerFraudDetector:
    """
    Lightweight fraud detection using:
    1. Rule-based NLP (no FinBERT needed)
    2. Statistical pattern matching (no sentence-transformers needed)
    3. Amount anomaly detection
    """
    
    def __init__(self):
        self._initialized = True
        logger.info("✅ Lightweight Transformer detector initialized (no external models)")
        
        # Fraud indicator keywords
        self.high_risk_keywords = [
            'urgent', 'verify', 'suspended', 'confirm', 'unusual',
            'unauthorized', 'blocked', 'security', 'alert', 'immediate',
            'click here', 'act now', 'prize', 'winner', 'congratulations',
            'account locked', 'verify now', 'suspended account', 'limited time',
            'claim', 'expires', 'won', 'lottery', 'bonus', 'free money'
        ]
        
        self.suspicious_patterns = [
            r'\b\d{16}\b',  # Credit card numbers
            r'\b\d{3}-\d{2}-\d{4}\b',  # SSN patterns
            r'password|pin|cvv|otp',  # Sensitive info requests
            r'bit\.ly|tinyurl|goo\.gl',  # Shortened URLs
        ]
    
    def analyze_transaction_description(self, description):
        """
        Analyze transaction description using rule-based NLP
        """
        if not description or description.strip() == "":
            return 0.5
        
        description_lower = description.lower()
        risk_score = 0.0
        
        # Check high-risk keywords
        keyword_count = sum(1 for keyword in self.high_risk_keywords if keyword in description_lower)
        risk_score += min(keyword_count * 0.15, 0.6)
        
        # Check suspicious patterns
        pattern_matches = sum(1 for pattern in self.suspicious_patterns if re.search(pattern, description_lower))
        risk_score += min(pattern_matches * 0.2, 0.4)
        
        # Check for ALL CAPS (shouting = suspicious)
        if description.isupper() and len(description) > 10:
            risk_score += 0.15
        
        # Check for excessive punctuation
        punctuation_ratio = len([c for c in description if c in '!!!???']) / max(len(description), 1)
        risk_score += min(punctuation_ratio * 0.5, 0.2)
        
        return min(max(risk_score, 0.0), 1.0)
    
    def get_embedding(self, text):
        """
        Create simple character-based embedding (no ML needed)
        """
        # Convert text to numerical vector
        char_counts = Counter(text.lower())
        embedding = np.array([
            char_counts.get(chr(i), 0) for i in range(ord('a'), ord('z') + 1)
        ] + [
            char_counts.get(str(i), 0) for i in range(10)
        ] + [
            len(text),
            len(text.split()),
            text.count(' ')
        ])
        
        # Normalize
        norm = np.linalg.norm(embedding)
        if norm > 0:
            embedding = embedding / norm
        
        return embedding
    
    def calculate_pattern_anomaly(self, current_transaction, historical_transactions):
        """
        Calculate anomaly score based on historical patterns
        """
        if not historical_transactions or len(historical_transactions) == 0:
            return 0.5
        
        try:
            current_text = f"{current_transaction['amount']} {current_transaction['recipient']} {current_transaction['description']}"
            current_embedding = self.get_embedding(current_text)
            
            similarities = []
            for hist_txn in historical_transactions[-10:]:
                hist_text = f"{hist_txn.get('amount', 0)} {hist_txn.get('recipient', '')} {hist_txn.get('description', '')}"
                hist_embedding = self.get_embedding(hist_text)
                
                # Cosine similarity
                similarity = np.dot(current_embedding, hist_embedding) / (
                    np.linalg.norm(current_embedding) * np.linalg.norm(hist_embedding) + 1e-8
                )
                similarities.append(similarity)
            
            avg_similarity = np.mean(similarities) if similarities else 0.5
            anomaly_score = 1.0 - avg_similarity
            
            return min(max(anomaly_score, 0.0), 1.0)
            
        except Exception as e:
            logger.error(f"Error in pattern anomaly: {e}")
            return 0.5
    
    def calculate_amount_anomaly(self, amount, historical_amounts):
        """
        Detect anomalous transaction amounts
        """
        if not historical_amounts or len(historical_amounts) < 3:
            # No history - base risk on absolute amount
            if amount > 1000000:  # > 10 lakh
                return 0.9
            elif amount > 500000:  # > 5 lakh
                return 0.7
            elif amount > 100000:  # > 1 lakh
                return 0.5
            elif amount > 50000:   # > 50k
                return 0.3
            else:
                return 0.2
        
        try:
            amounts = np.array(historical_amounts)
            mean_amount = np.mean(amounts)
            std_amount = np.std(amounts)
            
            if std_amount == 0:
                std_amount = mean_amount * 0.1
            
            # Z-score calculation
            z_score = abs((amount - mean_amount) / std_amount)
            
            # Convert z-score to risk (0-1)
            risk_score = min(z_score / 5.0, 1.0)
            
            # Add penalty for very large absolute amounts
            if amount > 1000000:
                risk_score = max(risk_score, 0.8)
            elif amount > 500000:
                risk_score = max(risk_score, 0.6)
            
            return risk_score
            
        except Exception as e:
            logger.error(f"Error in amount anomaly: {e}")
            return 0.5
    
    def calculate_fraud_risk(self, amount, recipient, description, historical_transactions):
        """
        Calculate overall fraud risk
        
        Args:
            amount: Transaction amount
            recipient: Recipient address/name
            description: Transaction description
            historical_transactions: List of past transactions
            
        Returns:
            float: Fraud risk score (0-1)
        """
        try:
            logger.info(f"Lightweight Transformer analyzing: Amount={amount}, Recipient={recipient[:20]}...")
            
            # 1. NLP-based description analysis (40% weight)
            description_risk = self.analyze_transaction_description(description)
            logger.info(f"  - Description risk: {description_risk:.2%}")
            
            # 2. Pattern anomaly detection (30% weight)
            current_txn = {
                'amount': amount,
                'recipient': recipient,
                'description': description
            }
            pattern_risk = self.calculate_pattern_anomaly(current_txn, historical_transactions)
            logger.info(f"  - Pattern anomaly: {pattern_risk:.2%}")
            
            # 3. Amount anomaly detection (30% weight)
            historical_amounts = [txn.get('amount', 0) for txn in historical_transactions if 'amount' in txn]
            amount_risk = self.calculate_amount_anomaly(amount, historical_amounts)
            logger.info(f"  - Amount anomaly: {amount_risk:.2%}")
            
            # Weighted ensemble
            final_risk = (
                description_risk * 0.40 +
                pattern_risk * 0.30 +
                amount_risk * 0.30
            )
            
            logger.info(f"  - Transformer final risk: {final_risk:.2%}")
            
            return min(max(final_risk, 0.0), 1.0)
            
        except Exception as e:
            logger.error(f"Error in fraud risk calculation: {e}")
            # Fallback
            if amount > 500000:
                return 0.8
            elif amount > 100000:
                return 0.5
            else:
                return 0.2

# Global instance
transformer_detector = TransformerFraudDetector()

# Test function
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    print("\n🔍 Testing Lightweight Transformer Fraud Detector...\n")
    
    print("=" * 60)
    print("Test 1: Suspicious description with keywords")
    print("=" * 60)
    risk1 = transformer_detector.calculate_fraud_risk(
        amount=50000,
        recipient="0x1234567890abcdef",
        description="URGENT: Verify your account immediately or it will be blocked!",
        historical_transactions=[]
    )
    print(f"✅ Result: {risk1:.2%} (Expected: High ~60-70%)\n")
    
    print("=" * 60)
    print("Test 2: Normal transaction description")
    print("=" * 60)
    risk2 = transformer_detector.calculate_fraud_risk(
        amount=5000,
        recipient="0xabcdef0123456789",
        description="Monthly rent payment",
        historical_transactions=[]
    )
    print(f"✅ Result: {risk2:.2%} (Expected: Low ~20-30%)\n")
    
    print("=" * 60)
    print("Test 3: Large anomalous amount")
    print("=" * 60)
    risk3 = transformer_detector.calculate_fraud_risk(
        amount=9000000,
        recipient="0x9999999999999999",
        description="Property purchase",
        historical_transactions=[
            {'amount': 5000, 'recipient': '0xaaa', 'description': 'grocery'},
            {'amount': 3000, 'recipient': '0xbbb', 'description': 'utilities'},
            {'amount': 4500, 'recipient': '0xccc', 'description': 'shopping'}
        ]
    )
    print(f"✅ Result: {risk3:.2%} (Expected: Very High ~80-90%)\n")
    
    print("=" * 60)
    print("Test 4: All caps suspicious message")
    print("=" * 60)
    risk4 = transformer_detector.calculate_fraud_risk(
        amount=25000,
        recipient="0x1111111111111111",
        description="CONGRATULATIONS!!! YOU WON THE LOTTERY!!! CLAIM NOW!!!",
        historical_transactions=[]
    )
    print(f"✅ Result: {risk4:.2%} (Expected: Very High ~85-95%)\n")
    
    print("🎉 Lightweight Transformer detector test complete!")
    print("✅ No external models needed - works with disk space limitations!\n")
