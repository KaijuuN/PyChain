from flask import Flask, jsonify, request
from blockchain import Blockchain
from pychaindatabase import save_blockchain, load_blockchain, save_wallet, load_wallets
from transactionpool import TransactionPool
from transactions import MultiSigTransaction, Transaction
from wallet import MultiSigWallet, Wallet
from miner import Miner

app = Flask(__name__)

# Initialisiere Blockchain und Wallets
blockchain = load_blockchain()  # Lade Blockchain aus der Datenbank
transaction_pool = TransactionPool()
miner = Miner(blockchain, transaction_pool)

wallets = load_wallets()  # Lade vorhandene Wallets

# Mining eines neuen Blocks
@app.route('/mine/<miner_wallet>', methods=['GET'])
def mine(miner_wallet):
    if miner_wallet not in wallets:
        return 'Miner wallet not found', 400
    block = miner.mine(wallets[miner_wallet])
    save_blockchain(blockchain)  # Speichere die Blockchain nach dem Mining
    if block:
        return jsonify(block.to_dict()), 200
    else:
        return 'No transactions to mine', 200


# Hinzufügen einer neuen Transaktion
@app.route('/new_transaction', methods=['POST'])
def new_transaction():
    tx_data = request.get_json()
    sender_wallet = wallets.get(tx_data['sender'])
    receiver_wallet = wallets.get(tx_data['receiver'])

    if not sender_wallet or not receiver_wallet:
        return 'Invalid wallet addresses', 400

    transaction = Transaction(sender_wallet, receiver_wallet, tx_data['amount'])
    transaction_pool.add_transaction(transaction, blockchain)
    save_blockchain(blockchain)  # Speichere die Blockchain nach der Transaktion

    return 'Transaction added', 201


# Abrufen der gesamten Blockchain
@app.route('/chain', methods=['GET'])
def get_chain():
    chain_data = [block.to_dict() for block in blockchain.chain]
    return jsonify(chain_data), 200


# Guthaben eines Wallets abfragen
@app.route('/balance/<wallet_address>', methods=['GET'])
def get_balance(wallet_address):
    wallet = wallets.get(wallet_address)
    if not wallet:
        return jsonify({'error': 'Wallet not found'}), 404

    balance = wallet.get_balance(blockchain)
    return jsonify({'balance': balance}), 200


# Transaktionshistorie eines Wallets abfragen
@app.route('/transactions/<wallet_address>', methods=['GET'])
def get_transactions(wallet_address):
    wallet_transactions = []
    for block in blockchain.chain:
        for tx in block.transactions:
            if tx.sender == wallet_address or tx.receiver == wallet_address:
                wallet_transactions.append(tx.to_dict())

    if not wallet_transactions:
        return jsonify({'message': 'No transactions found for this wallet'}), 404

    return jsonify(wallet_transactions), 200


# Blockchain auf Validität prüfen
@app.route('/validate_chain', methods=['GET'])
def validate_chain():
    is_valid = blockchain.is_chain_valid()
    return jsonify({'valid': is_valid}), 200


# Neues Wallet erstellen
@app.route('/create_wallet', methods=['POST'])
def create_wallet():
    wallet_address = request.json.get('address')
    if wallet_address in wallets:
        return jsonify({'error': 'Wallet already exists'}), 400
    
    new_wallet = Wallet(blockchain, wallet_address)
    
    save_wallet(new_wallet)  # Speichere Wallets nach der Erstellung

    return jsonify({'message': f'Wallet {wallet_address} created successfully'}), 201


# Multi-Signature Wallet erstellen
@app.route('/create_multisig_wallet', methods=['POST'])
def create_multisig_wallet():
    data = request.get_json()
    owners = [wallets.get(owner) for owner in data['owners']]
    required_signatures = data['required_signatures']

    if None in owners:
        return 'Invalid wallet addresses', 400

    multisig_wallet = MultiSigWallet(blockchain, owners, required_signatures)
    save_wallet(wallets)  # Speichere Wallets nach der Erstellung eines MultiSig-Wallets

    return 'Multi-Signature Wallet created', 201


# Multi-Signature Transaktion hinzufügen
@app.route('/new_multisig_transaction', methods=['POST'])
def new_multisig_transaction():
    tx_data = request.get_json()
    sender_wallet = wallets.get(tx_data['sender'])
    receiver_wallet = wallets.get(tx_data['receiver'])
    signatures = tx_data['signatures']

    if not sender_wallet or not receiver_wallet:
        return 'Invalid wallet addresses', 400

    multisig_wallet = MultiSigWallet(blockchain, [sender_wallet], tx_data['required_signatures'])
    transaction = MultiSigTransaction(sender_wallet, receiver_wallet, tx_data['amount'], signatures)

    if not transaction.is_valid(multisig_wallet):
        return 'Not enough valid signatures', 400

    transaction_pool.add_transaction(transaction, blockchain)
    save_blockchain(blockchain)  # Speichere Blockchain nach MultiSig-Transaktion

    return 'Multi-Signature Transaction added', 201


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
