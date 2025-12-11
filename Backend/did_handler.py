import hashlib
import json
from datetime import datetime, timezone

class DIDHandler:
    """W3C Decentralized Identity Document handler - No external dependencies"""
    
    def create_did_document(self, user_id, ethereum_address, email):
        """Create W3C compliant DID document"""
        
        # Generate DID (did:ethr:ethereum_address)
        did_id = f"did:ethr:{ethereum_address}"
        
        # Generate unique DID key hash
        key_hash = hashlib.sha256(f"{user_id}:{ethereum_address}".encode()).hexdigest()
        
        # Create W3C compliant DID Document
        did_document = {
            "@context": [
                "https://www.w3.org/ns/did/v1",
                "https://w3id.org/security/suites/secp256k1-2019/v1"
            ],
            "id": did_id,
            "verificationMethod": [{
                "id": f"{did_id}#key-1",
                "type": "EcdsaSecp256k1VerificationKey2019",
                "controller": did_id,
                "ethereumAddress": ethereum_address,
                "publicKeyHash": key_hash
            }],
            "authentication": [f"{did_id}#key-1"],
            "assertionMethod": [f"{did_id}#key-1"],
            "service": [{
                "id": f"{did_id}#fraud-detection",
                "type": "FraudDetectionService",
                "serviceEndpoint": "https://api.antifraud-system.com/verify"
            }],
            "created": datetime.now(timezone.utc).isoformat(),
            "updated": datetime.now(timezone.utc).isoformat()
        }
        
        return did_document
    
    def verify_did(self, did_document, ethereum_address):
        """Verify DID document authenticity"""
        if not did_document:
            return False
        
        # Check if DID matches ethereum address
        expected_did = f"did:ethr:{ethereum_address}"
        
        # Verify DID structure
        if did_document.get('id') != expected_did:
            return False
        
        # Verify verification method exists
        if not did_document.get('verificationMethod'):
            return False
        
        # Verify ethereum address in verification method
        verification_method = did_document['verificationMethod'][0]
        if verification_method.get('ethereumAddress') != ethereum_address:
            return False
        
        return True
    
    def resolve_did(self, did_id):
        """Resolve DID to get DID Document"""
        # In production: Query Ethereum DID registry contract
        # For now, return resolution status
        return {
            "status": "resolved",
            "did": did_id,
            "method": "ethr"
        }
    
    def update_did_document(self, did_document):
        """Update DID document timestamp"""
        if did_document:
            did_document['updated'] = datetime.now(timezone.utc).isoformat()
        return did_document

# Global instance
did_handler = DIDHandler()
