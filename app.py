from flask import Flask, jsonify, request
from blockchain import Blockchain  # Deine existierende Blockchain importieren

app = Flask(__name__)

# Erstelle eine Instanz der bestehenden Blockchain
blockchain = Blockchain()

# Mining eines neuen Blocks
@app.route('/mine', methods=['GET'])
def mine():
    block = blockchain.mine_pending_transactions('MinerAddress')
    return jsonify(block.__dict__), 200

# Hinzufügen einer neuen Transaktion
@app.route('/new_transaction', methods=['POST'])
def new_transaction():
    tx_data = request.get_json()
    blockchain.add_transaction(tx_data['sender'], tx_data['receiver'], tx_data['amount'])
    return 'Transaction added', 201

# Abrufen der gesamten Blockchain
@app.route('/chain', methods=['GET'])
def get_chain():
    chain_data = [block.__dict__ for block in blockchain.chain]
    return jsonify(chain_data), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
