from flask import Flask, jsonify, request
from blockchain import Blockchain  # Deine existierende Blockchain importieren
from transactionpool import TransactionPool
from transactions import Transaction
from wallet import Wallet
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
}

# Initiale Guthaben für die Wallets
Transaction.credit_wallet(wallets['wallet_1'], 500, transaction_pool, blockchain)
Transaction.credit_wallet(wallets['wallet_2'], 500, transaction_pool, blockchain)

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
