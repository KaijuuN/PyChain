class Wallet:
    def __init__(self, blockchain, address: str):
        self.blockchain = blockchain  # Verweis auf die Blockchain
        self.address = address  # Adresse des Wallets

    def get_balance(self, blockchain):
        """Berechne den Kontostand des Wallets basierend auf den Transaktionen in der Blockchain."""
        balance = 0

        # Durchlaufe alle Blöcke und Transaktionen der Blockchain
        for block in blockchain.chain:
            for tx in block.transactions:
                if tx.sender == self.address:
                    balance -= tx.amount
                if tx.receiver == self.address:
                    balance += tx.amount

        return balance

    def has_sufficient_balance(self, amount: float, blockchain) -> bool:
        """Prüft, ob das Wallet genügend Guthaben hat, um eine Transaktion auszuführen."""
        return self.get_balance(blockchain) >= amount

    def __repr__(self):
        return f"Wallet({self.address}): {self.get_balance(self.blockchain)}"
