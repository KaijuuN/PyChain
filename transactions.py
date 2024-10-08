from wallet import Wallet, MultiSigWallet


class Transaction:
    def __init__(self, sender: Wallet, receiver: Wallet, amount: float):
        self.sender_wallet = sender  # Speichere das Wallet-Objekt des Senders
        self.receiver_wallet = receiver  # Speichere das Wallet-Objekt des Empfängers

        self.sender = sender.address if sender is not None else "System"
        self.receiver = receiver.address
        self.amount = amount

    def to_dict(self):
        """Konvertiert die Transaktion in ein Dictionary (für das Speichern oder Anzeigen)."""
        return {
            "sender": self.sender,
            "receiver": self.receiver,
            "amount": self.amount
        }

    @staticmethod
    def credit_wallet(receiver_wallet, amount, transaction_pool, blockchain):
        """Erstellt eine System-Transaktion und fügt sie dem Pool hinzu."""
        system_transaction = Transaction(None, receiver_wallet, amount)
        transaction_pool.add_transaction(system_transaction, blockchain)
        # print(f"[DEBUG] {amount} wurde dem Wallet {receiver_wallet.address} gutgeschrieben.")

    def __repr__(self):
        return f"Transaction(from: {self.sender}, to: {self.receiver}, amount: {self.amount})"

class MultiSigTransaction(Transaction):
    def __init__(self, sender_wallet, receiver_wallet, amount, signatures: list):
        super().__init__(sender_wallet, receiver_wallet, amount)
        self.signatures = signatures

    def is_valid(self, multisig_wallet: MultiSigWallet) -> bool:
        return multisig_wallet.verify_signatures(self.signatures)
