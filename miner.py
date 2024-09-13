import time
from block import Block
from blockchain import Blockchain
from transactionpool import TransactionPool
from transactions import Transaction
from wallet import Wallet


class Miner:
    def __init__(self, blockchain: Blockchain, transaction_pool: TransactionPool):
        self.blockchain = blockchain
        self.transaction_pool = transaction_pool

    def mine(self, miner_wallet: Wallet, reward: float = 10):
        """Mined ausstehende Transaktionen und belohnt den Miner."""
        transactions = self.transaction_pool.get_pending_transactions()

        # Füge eine Belohnungstransaktion für den Miner hinzu
        reward_transaction = Transaction(None, miner_wallet, reward)
        transactions.append(reward_transaction)

        # Prüfen, ob es Transaktionen zu minen gibt
        if len(transactions) == 0:
            print("Keine Transaktionen zum Minen.")
            return None

        # Erstelle einen neuen Block mit den Transaktionen
        new_block = Block(len(self.blockchain.chain),
                          self.blockchain.get_latest_block().hash, transactions)

        # Mining-Prozess: Wir finden eine Nonce, die den Block-Hash gültig macht
        target = "0" * self.blockchain.difficulty
        while not new_block.hash or not new_block.hash.startswith(target):
            new_block.nonce += 1
            new_block.hash = new_block.calculate_hash()

        # Füge den Block zur Blockchain hinzu
        self.blockchain.add_block(new_block)
        return new_block
