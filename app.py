from flask import Flask, jsonify, request
from blockchain import Blockchain  # Deine existierende Blockchain importieren
from transactionpool import TransactionPool
from transactions import MultiSigTransaction, Transaction
from wallet import MultiSigWallet, Wallet
from miner import Miner

app = Flask(__name__)

# Erstelle eine Instanz der bestehenden Blockchain, des TransactionPools und des Miners
blockchain = Blockchain()
transaction_pool = TransactionPool()
miner = Miner(blockchain, transaction_pool)


# Beispiel-Wallets (in einem echten System wären sie dynamisch)
wallets = {
    'wallet_1': Wallet(blockchain, 'wallet_1'),
    'wallet_2': Wallet(blockchain, 'wallet_2'),
    'Kaijuu': Wallet(blockchain, 'Kaijuu'),
    'Angelina': Wallet(blockchain, 'Angelina'),
}


# Initiale Guthaben für die Wallets
Transaction.credit_wallet(wallets['wallet_1'], 500, transaction_pool, blockchain)
Transaction.credit_wallet(wallets['wallet_2'], 500, transaction_pool, blockchain)
Transaction.credit_wallet(wallets['Kaijuu'], 500, transaction_pool, blockchain)
Transaction.credit_wallet(wallets['Angelina'], 500, transaction_pool, blockchain)


# Mining eines neuen Blocks
@app.route('/mine', methods=['GET'])
def mine():
    miner_wallet = Wallet(blockchain, "Miner69er")  # Beispiel Miner Wallet
    block = miner.mine(miner_wallet)  # Miner nutzt das Mining
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

    return 'Transaction added', 201


# Abrufen der gesamten Blockchain
@app.route('/chain', methods=['GET'])
def get_chain():
    chain_data = [block.to_dict() for block in blockchain.chain]
    return jsonify(chain_data), 200


# Neue Route, um das Guthaben eines Wallets abzufragen
@app.route('/balance/<wallet_address>', methods=['GET'])
def get_balance(wallet_address):
    wallet = wallets.get(wallet_address)
    if not wallet:
        return jsonify({'error': 'Wallet not found'}), 404

    balance = wallet.get_balance(blockchain)
    return jsonify({'balance': balance}), 200


# Neue Route, um die Transaktionshistorie eines Wallets abzufragen
@app.route('/transactions/<wallet_address>', methods=['GET'])
def get_transactions(wallet_address):
    wallet_transactions = []
    for block in blockchain.chain:
        for tx in block.transactions:
            if tx.sender == wallet_address or tx.receiver == wallet_address:
                wallet_transactions.append(tx.to_dict())

    if len(wallet_transactions) == 0:
        return jsonify({'message': 'No transactions found for this wallet'}), 404

    return jsonify(wallet_transactions), 200


# Neue Route, um die Blockchain auf Validität zu prüfen
@app.route('/validate_chain', methods=['GET'])
def validate_chain():
    is_valid = blockchain.is_chain_valid()
    return jsonify({'valid': is_valid}), 200


# Neue Route, um ein neues Wallet zu erstellen
@app.route('/create_wallet', methods=['POST'])
def create_wallet():
    wallet_address = request.json.get('address')
    if wallet_address in wallets:
        return jsonify({'error': 'Wallet already exists'}), 400
    
    new_wallet = Wallet(blockchain, wallet_address)
    wallets[wallet_address] = new_wallet

    return jsonify({'message': f'Wallet {wallet_address} created successfully'}), 201


@app.route('/create_multisig_wallet', methods=['POST'])
def create_multisig_wallet():
    data = request.get_json()
    owners = [wallets[owner] for owner in data['owners']]  # Überprüfen, dass beide Wallets in der Liste sind
    required_signatures = data['required_signatures']

    if None in owners:
        return 'Invalid wallet addresses', 400

    multisig_wallet = MultiSigWallet(blockchain, owners, required_signatures)
    return 'Multi-Signature Wallet created', 201


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
    return 'Multi-Signature Transaction added', 201




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
