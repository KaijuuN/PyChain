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


class MultiSigWallet:
    def __init__(self, blockchain, owners: list, required_signatures: int):
        self.blockchain = blockchain
        self.owners = owners  # Liste der Besitzer-Adressen
        self.required_signatures = required_signatures  # Anzahl erforderlicher Signaturen

    def has_sufficient_balance(self, amount: float) -> bool:
        balance = sum([owner.get_balance(self.blockchain) for owner in self.owners])
        return balance >= amount

    def verify_signatures(self, signatures: list) -> bool:
        valid_signatures = []
        
        # Debug: Alle Signaturen und Besitzer ausgeben
        print("[DEBUG] Überprüfe Signaturen:")
        print(f"[DEBUG] Signaturen: {signatures}")
        print(f"[DEBUG] Besitzer: {[owner.address for owner in self.owners]}")

        # Überprüfe jede Signatur
        for sig in signatures:
            if sig in [owner.address for owner in self.owners]:
                valid_signatures.append(sig)
            else:
                print(f"[DEBUG] Ungültige Signatur: {sig}")

        print(f"[DEBUG] Gültige Signaturen: {valid_signatures}")
        return len(valid_signatures) >= self.required_signatures
