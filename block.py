import hashlib
import time
import json


class Block:
    def __init__(self, index: int, prev_hash: str, transactions: list):
        self.index = index
        self.timestamp = time.time()
        self.transactions = transactions
        self.prev_hash = prev_hash
        self.nonce = 0  # Nonce wird während des Minings gesetzt
        self._merkle_root = self.calculate_merkle_root()
        self.hash = None  # Der Hash wird während des Minings berechnet

    def calculate_hash(self) -> str:
        transactions_str = json.dumps(
            [tx.to_dict() for tx in self.transactions], sort_keys=True)
        block_str = f"{self.index}{self.timestamp}{transactions_str}{
            self.prev_hash}{self.nonce}{self.merkle_root}"
        return hashlib.sha256(block_str.encode()).hexdigest()

    @property
    def merkle_root(self) -> str:
        # Überprüfe, ob die Merkle-Root schon berechnet wurde
        if self._merkle_root is None:
            self._merkle_root = self.calculate_merkle_root()
        return self._merkle_root

    # Berechne die Merkle-Root der Transaktionen

    def calculate_merkle_root(self) -> str:
        # Hilfsfunktion, um einen String zu hashen
        def hash_string(s: str) -> str:
            return hashlib.sha256(s.encode()).hexdigest()

        # Hilfsfunktion, um zwei Hashes zu kombinieren und erneut zu hashen
        def hash_pair(h1: str, h2: str) -> str:
            return hashlib.sha256((h1 + h2).encode()).hexdigest()

        # Wenn keine Transaktionen vorhanden sind
        if len(self.transactions) == 0:
            return ""

        # Wenn nur eine Transaktion vorhanden ist, wird der Hash der Transaktion zurückgegeben
        if len(self.transactions) == 1:
            return hashlib.sha256(json.dumps(self.transactions[0].to_dict(), sort_keys=True).encode()).hexdigest()

        # Schritt 1: Transaktionen hashen
        transaction_hashes = [hash_string(json.dumps(
            tx.to_dict(), sort_keys=True)) for tx in self.transactions]

        # Schritt 2: Paare bilden und hashen, bis nur ein Hash übrig ist
        while len(transaction_hashes) > 1:
            # Wenn wir eine ungerade Anzahl an Hashes haben, duplizieren wir den letzten Hash
            if len(transaction_hashes) % 2 != 0:
                transaction_hashes.append(transaction_hashes[-1])

            # Paare bilden und erneut hashen
            new_hashes = []
            for i in range(0, len(transaction_hashes), 2):
                new_hash = hash_pair(
                    transaction_hashes[i], transaction_hashes[i + 1])
                new_hashes.append(new_hash)

            transaction_hashes = new_hashes

        # Der letzte verbliebene Hash ist die Merkle-Root
        return transaction_hashes[0]
