from typing import List
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization



class Wallet:
    def __init__(self, blockchain, address: str):
        self.blockchain = blockchain  # Verweis auf die Blockchain
        self.address: str = address  # Adresse des Wallets
        # Generiere ein Schlüsselpaar
        self.private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )
        self.public_key = self.private_key.public_key()

    def get_balance(self) -> float:
        """Berechne den Kontostand des Wallets basierend auf den Transaktionen in der Blockchain."""
        balance: float = 0.0

        # Durchlaufe alle Blöcke und Transaktionen der Blockchain
        for block in self.blockchain.chain:
            for tx in block.transactions:
                if tx.sender == self.address:
                    balance -= tx.amount
                if tx.receiver == self.address:
                    balance += tx.amount

        return balance

    def has_sufficient_balance(self, amount: float, blockchain) -> bool:
        """Prüft, ob das Wallet genügend Guthaben hat, um eine Transaktion auszuführen."""
        return self.get_balance(blockchain) >= amount
    
    def export_keys(self) -> dict:
        """Exportiere die Schlüssel als serialisierte Werte (z.B. um sie in einer Datei zu speichern)."""
        private_pem = self.private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        )
        public_pem = self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        return {"private_key": private_pem.decode('utf-8'), "public_key": public_pem.decode('utf-8')}

    def __repr__(self) -> str:
        return f"Wallet({self.address}): {self.get_balance(self.blockchain)}"


class MultiSigWallet:
    def __init__(self, blockchain, owners: List[Wallet], required_signatures: int):
        self.blockchain = blockchain
        self.owners: List[Wallet] = owners  # Liste der Besitzer-Wallets
        self.required_signatures: int = required_signatures  # Anzahl erforderlicher Signaturen

    def has_sufficient_balance(self, amount: float) -> bool:
        """Prüft, ob die Besitzer genügend Guthaben haben, um eine Transaktion auszuführen."""
        balance: float = sum(owner.get_balance(self.blockchain) for owner in self.owners)
        return balance >= amount

    def verify_signatures(self, signatures: List[str]) -> bool:
        """Überprüft, ob genügend gültige Signaturen vorhanden sind."""
        valid_signatures: List[str] = []

        # Debugging-Informationen
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
