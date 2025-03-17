from web3 import Web3
from eth_account import Account
import json
import os

def deploy_contract():
    # Connect to local Ethereum node
    w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))
    
    # Load account credentials
    account = Account.from_key(os.getenv('ETHEREUM_PRIVATE_KEY'))
    
    # Load contract bytecode and ABI
    with open('MedicalRecord.json') as f:
        contract_json = json.load(f)
        contract_bytecode = contract_json['bytecode']
        contract_abi = contract_json['abi']
    
    # Create contract instance
    Contract = w3.eth.contract(abi=contract_abi, bytecode=contract_bytecode)
    
    # Get nonce
    nonce = w3.eth.get_transaction_count(account.address)
    
    # Build transaction
    transaction = Contract.constructor().build_transaction({
        'chainId': 1337,  # Local testnet
        'gas': 2000000,
        'gasPrice': w3.eth.gas_price,
        'nonce': nonce,
    })
    
    # Sign transaction
    signed_txn = w3.eth.account.sign_transaction(transaction, account.key)
    
    # Send transaction
    tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    
    # Wait for transaction receipt
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    
    # Save contract address and ABI
    contract_data = {
        'address': tx_receipt['contractAddress'],
        'abi': contract_abi
    }
    
    with open('MedicalRecord.json', 'w') as f:
        json.dump(contract_data, f, indent=4)
    
    print(f"Contract deployed at: {tx_receipt['contractAddress']}")

if __name__ == '__main__':
    deploy_contract() 