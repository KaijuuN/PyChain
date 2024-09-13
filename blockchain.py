
from block import Block
from wallet import Wallet


class Blockchain:
    def __init__(self):
        self.chain = []  # Initialisiert eine leere liste

        if len(self.chain) == 0:
            self.create_genesis_block()

    def create_genesis_block(self):
        """Erstellt den ersten Block der Blockchain."""
        if len(self.chain) > 0:
            return  # Genesis-Block existiert bereits

        # Erstelle den Genesis-Block mit Index 0 und einem speziellen "GENESIS" Hash
        genesis_block = Block(0, "GENESIS BLOCK", [])
        # Berechne den Hash für den Genesis-Block
        genesis_block.hash = genesis_block.calculate_hash()

        # Füge den Genesis-Block zur Blockchain hinzu
        self.chain.append(genesis_block)

    def get_latest_block(self):
        return self.chain[-1] if self.chain else None

    def add_block(self, new_block: Block):
        """Fügt einen neuen Block zur Blockchain hinzu."""
        if len(self.chain) > 0:
            new_block.prev_hash = self.get_latest_block().hash
        new_block.hash = new_block.calculate_hash()  # Berechne den Hash für den Block
        self.chain.append(new_block)

    def get_balance_of_address(self, address: Wallet) -> float:
        balance = 0

        # Gehe durch jeden Block in der Blockchain
        for block in self.chain:
            # Gehe durch jede Transaktion in diesem Block
            for tx in block.transactions:
                if tx.sender == address:
                    # Wenn die Adresse der Absender ist, ziehe den Betrag ab
                    balance -= tx.amount
                if tx.receiver == address:
                    # Wenn die Adresse der Empfänger ist, füge den Betrag hinzu
                    balance += tx.amount

        return balance

    def is_chain_valid(self) -> bool:
        # Beginne bei Block 1, da Block 0 der Genesis-Block ist
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            prev_block = self.chain[i - 1]

            # Überprüfe, ob der Hash des aktuellen Blocks korrekt ist
            if current_block.hash != current_block.calculate_hash():
                print(f"Invalid hash at block {current_block.index}")
                return False

            # Überprüfe, ob der prev_hash mit dem Hash des vorherigen Blocks übereinstimmt
            if current_block.prev_hash != prev_block.hash:
                print(f"Invalid prev_hash linkage at block {
                      current_block.index}")
                return False

        return True
