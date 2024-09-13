from block import Block
from blockchain import Blockchain
from transactionpool import TransactionPool
from transactions import Transaction
from wallet import Wallet


class Miner:
    def __init__(self, blockchain: Blockchain, transaction_pool: TransactionPool):
        self.blockchain = blockchain
        self.transaction_pool = transaction_pool

    def mine(self, miner_wallet: Wallet, reward: float = 100):
        """Mined ausstehende Transaktionen und belohnt den Miner."""
        # Hole die ausstehenden Transaktionen
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

        # Füge den Block zur Blockchain hinzu
        self.blockchain.add_block(new_block)

        print(f"[DEBUG] Transaktionen im Block {new_block.index}:")
        for tx in new_block.transactions:
            print(tx)

        print(f"Block {new_block.index} erfolgreich gemined.")
        return new_block
