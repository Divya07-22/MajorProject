# zkp/generate_proof.py
import subprocess
import json
import os

class ZKProofGenerator:
    """Generate zero-knowledge proofs for risk scores"""
    
    def __init__(self, zkp_dir='zkp'):
        self.zkp_dir = zkp_dir
    
    def generate_proof(self, risk_score, threshold=85):
        """
        Generate a ZK proof that risk_score >= threshold
        
        Args:
            risk_score: Risk score (0-100)
            threshold: Threshold for fraud (default 85)
        
        Returns:
            dict: Proof data including proof and public inputs
        """
        try:
            # Navigate to zkp directory
            os.chdir(self.zkp_dir)
            
            # Compute witness
            print(f"Computing witness for risk_score={risk_score}, threshold={threshold}")
            witness_cmd = f"zokrates compute-witness -a {risk_score} {threshold}"
            subprocess.run(witness_cmd, shell=True, check=True)
            
            # Generate proof
            print("Generating proof...")
            proof_cmd = "zokrates generate-proof"
            subprocess.run(proof_cmd, shell=True, check=True)
            
            # Read proof
            with open('proof.json', 'r') as f:
                proof_data = json.load(f)
            
            # Navigate back
            os.chdir('..')
            
            print("✅ Proof generated successfully!")
            return proof_data
        
        except Exception as e:
            print(f"❌ Proof generation failed: {e}")
            os.chdir('..')
            return None
    
    def format_proof_for_solidity(self, proof_data):
        """
        Format proof data for Solidity contract call
        
        Args:
            proof_data: Proof JSON data
        
        Returns:
            tuple: (a, b, c, input) formatted for Solidity
        """
        proof = proof_data['proof']
        inputs = proof_data['inputs']
        
        a = [proof['a'][0], proof['a'][1]]
        b = [[proof['b'][0][0], proof['b'][0][1]], 
             [proof['b'][1][0], proof['b'][1][1]]]
        c = [proof['c'][0], proof['c'][1]]
        
        return a, b, c, inputs

# Example usage
if __name__ == "__main__":
    generator = ZKProofGenerator()
    
    # Generate proof for high risk score
    risk_score = 92
    threshold = 85
    
    proof_data = generator.generate_proof(risk_score, threshold)
    
    if proof_data:
        a, b, c, inputs = generator.format_proof_for_solidity(proof_data)
        print("\nFormatted for Solidity:")
        print(f"a: {a}")
        print(f"b: {b}")
        print(f"c: {c}")
        print(f"inputs: {inputs}")
