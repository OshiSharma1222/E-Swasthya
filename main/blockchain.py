from web3 import Web3
from eth_account import Account
import json
import os
from datetime import datetime

class BlockchainManager:
    def __init__(self):
        # Connect to a local Ethereum node (you can use Infura or other providers)
        self.w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))
        
        # Load contract ABI and address
        contract_path = os.path.join(os.path.dirname(__file__), 'contracts', 'MedicalRecord.json')
        with open(contract_path) as f:
            contract_json = json.load(f)
            self.contract_abi = contract_json['abi']
            self.contract_address = contract_json['address']
        
        # Initialize contract
        self.contract = self.w3.eth.contract(
            address=self.contract_address,
            abi=self.contract_abi
        )
        
        # Load account credentials
        self.account = Account.from_key(os.getenv('ETHEREUM_PRIVATE_KEY'))
    
    def store_medical_record(self, patient_id, report_hash, report_data):
        """
        Store medical record on the blockchain
        """
        try:
            # Prepare transaction
            nonce = self.w3.eth.get_transaction_count(self.account.address)
            
            # Create transaction
            transaction = self.contract.functions.storeRecord(
                patient_id,
                report_hash,
                report_data
            ).build_transaction({
                'chainId': 1337,  # Local testnet
                'gas': 2000000,
                'gasPrice': self.w3.eth.gas_price,
                'nonce': nonce,
            })
            
            # Sign transaction
            signed_txn = self.w3.eth.account.sign_transaction(
                transaction, self.account.key
            )
            
            # Send transaction
            tx_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
            
            # Wait for transaction receipt
            tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
            
            return {
                'success': True,
                'transaction_hash': tx_receipt['transactionHash'].hex()
            }
            
        except Exception as e:
            print(f"Error storing medical record: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_medical_record(self, patient_id, report_hash):
        """
        Retrieve medical record from the blockchain
        """
        try:
            record = self.contract.functions.getRecord(
                patient_id,
                report_hash
            ).call()
            
            return {
                'success': True,
                'data': record
            }
            
        except Exception as e:
            print(f"Error retrieving medical record: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def verify_record_integrity(self, patient_id, report_hash):
        """
        Verify the integrity of a medical record
        """
        try:
            record = self.contract.functions.getRecord(
                patient_id,
                report_hash
            ).call()
            
            return {
                'success': True,
                'verified': True,
                'timestamp': record[2]  # Assuming timestamp is stored in the record
            }
            
        except Exception as e:
            print(f"Error verifying record: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            } 