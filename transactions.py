from wallet import Wallet


class Transaction:
    def __init__(self, sender: Wallet, receiver: Wallet, amount: float):
        self.sender_wallet = sender  # Speichere das Wallet-Objekt des Senders
        self.receiver_wallet = receiver  # Speichere das Wallet-Objekt des Empfängers
        self.amount = amount
        # Speichere die Adressen der Wallets zur Serialisierung und Anzeige
        self.sender = sender.address if sender is not None else "System"
        self.receiver = receiver.address

    def to_dict(self):
        """Konvertiert die Transaktion in ein Dictionary (für das Speichern oder Anzeigen)."""
        return {
            "sender": self.sender,
            "receiver": self.receiver,
            "amount": self.amount
        }

    def __repr__(self):
        return f"Transaction(from: {self.sender}, to: {self.receiver}, amount: {self.amount})"
