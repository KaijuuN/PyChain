from block import Block
from blockchain import Blockchain
from transactionpool import TransactionPool
from transactions import Transaction
from wallet import Wallet


class Miner:
    def __init__(self, blockchain: Blockchain, transaction_pool: TransactionPool):
        self.blockchain = blockchain
        self.transaction_pool = transaction_pool

    def mine(self, miner_wallet: Wallet):
        """Mined ausstehende Transaktionen und belohnt den Miner."""
        # Hole die ausstehenden Transaktionen
        transactions = self.transaction_pool.get_pending_transactions()

        # Belohne den Miner mit einer Transaktion
        reward_transaction = Transaction(None, miner_wallet, 100)
        transactions.append(reward_transaction)

        # Erstelle einen neuen Block mit den Transaktionen
        new_block = Block(len(self.blockchain.chain),
                          self.blockchain.get_latest_block().hash, transactions)
        self.blockchain.add_block(new_block)
