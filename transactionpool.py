from transactions import Transaction


class TransactionPool:
    def __init__(self):
        self.pending_transactions = []

    def add_transaction(self, transaction: Transaction, blockchain):
        """Fügt eine neue Transaktion dem Pool hinzu, nachdem das Guthaben überprüft wurde."""
        # Überprüfe, ob der Sender genügend Guthaben hat
        if transaction.sender_wallet is not None:
            if not transaction.sender_wallet.has_sufficient_balance(transaction.amount, blockchain):
                raise ValueError(f"Nicht genügend Guthaben im Wallet von {
                    transaction.sender_wallet.address}.")
        self.pending_transactions.append(transaction)

    def get_pending_transactions(self):
        """Gibt die ausstehenden Transaktionen zurück und leert den Pool."""
        transactions = self.pending_transactions
        self.pending_transactions = []  # Leert den Pool nach dem Mining
        return transactions
