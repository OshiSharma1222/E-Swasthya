from web3 import Web3
from django.conf import settings
import json
import os
from datetime import datetime

class BlockchainService:
    def __init__(self):
        # Connect to local Ethereum node (Ganache)
        self.w3 = Web3(Web3.HTTPProvider(settings.BLOCKCHAIN_CONFIG['PROVIDER_URL']))
        
        # Load contract ABI and address
        contract_path = os.path.join(settings.BASE_DIR, 'build', 'contracts', 'MedicalRecord.json')
        with open(contract_path) as f:
            contract_data = json.load(f)
            self.contract_abi = contract_data['abi']
            # Get the most recent deployment address
            self.contract_address = contract_data['networks'][list(contract_data['networks'].keys())[-1]]['address']
            
            # Update settings with contract address
            settings.BLOCKCHAIN_CONFIG['CONTRACT_ADDRESS'] = self.contract_address
        
        # Initialize contract
        self.contract = self.w3.eth.contract(
            address=self.contract_address,
            abi=self.contract_abi
        )
        
        # Set up account with private key
        account = self.w3.eth.account.from_key(settings.BLOCKCHAIN_CONFIG['PRIVATE_KEY'])
        self.w3.eth.default_account = account.address
    
    def store_medical_record(self, patient_id, report_hash, report_data):
        """
        Store a medical record on the blockchain
        """
        try:
            # Call contract function
            tx_hash = self.contract.functions.storeRecord(
                patient_id,
                report_hash,
                report_data
            ).transact()
            
            # Wait for transaction to be mined
            tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
            
            return {
                'success': True,
                'transaction_hash': tx_receipt['transactionHash'].hex(),
                'block_number': tx_receipt['blockNumber']
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_medical_record(self, patient_id, report_hash):
        """
        Retrieve a medical record from the blockchain
        """
        try:
            record = self.contract.functions.getRecord(
                patient_id,
                report_hash
            ).call()
            
            return {
                'success': True,
                'data': {
                    'patient_id': record[0],
                    'report_hash': record[1],
                    'report_data': record[2],
                    'timestamp': datetime.fromtimestamp(record[3]),
                    'is_valid': record[4]
                }
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def update_medical_record(self, patient_id, report_hash, new_report_data):
        """
        Update an existing medical record
        """
        try:
            tx_hash = self.contract.functions.updateRecord(
                patient_id,
                report_hash,
                new_report_data
            ).transact()
            
            tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
            
            return {
                'success': True,
                'transaction_hash': tx_receipt['transactionHash'].hex(),
                'block_number': tx_receipt['blockNumber']
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def invalidate_medical_record(self, patient_id, report_hash):
        """
        Invalidate a medical record
        """
        try:
            tx_hash = self.contract.functions.invalidateRecord(
                patient_id,
                report_hash
            ).transact()
            
            tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
            
            return {
                'success': True,
                'transaction_hash': tx_receipt['transactionHash'].hex(),
                'block_number': tx_receipt['blockNumber']
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def verify_record_integrity(self, patient_id, report_hash):
        """
        Verify if a medical record is valid
        """
        try:
            is_valid = self.contract.functions.isRecordValid(
                patient_id,
                report_hash
            ).call()
            
            return {
                'success': True,
                'is_valid': is_valid
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            } 