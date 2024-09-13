from block import Block
from wallet import Wallet


class Blockchain:
    def __init__(self):
        self.chain = []  # Initialisiert eine leere liste
        self.difficulty = 3  # Eine festgelegte Schwierigkeit für das Mining
        self.block_time_target = 10  # Zielzeit pro block in sek
        # nach wie vielen Blöcke soll die schwierigkeit angepasst werden
        self.adjustment_interval = 10

        if len(self.chain) == 0:
            self.create_genesis_block()

    def create_genesis_block(self):
        """Erstellt den ersten Block der Blockchain."""
        if len(self.chain) > 0:
            return  # Genesis-Block existiert bereits
        genesis_block = Block(0, "GENESIS BLOCK", [])
        genesis_block.hash = genesis_block.calculate_hash()
        self.chain.append(genesis_block)

    def get_latest_block(self):
        return self.chain[-1] if self.chain else None

    def add_block(self, new_block: Block):
        """Fügt einen neuen Block zur Blockchain hinzu."""
        if len(self.chain) > 0:
            new_block.prev_hash = self.get_latest_block().hash
        self.chain.append(new_block)

        if len(self.chain) % self.adjustment_interval == 0:
            self.adjust_difficulty()

    def adjust_difficulty(self):
        """Passt die Mining-Schwierigkeit basierend auf der Zeit zwischen den letzten Blöcken an."""
        # Berechne die tatsächliche Zeit, die für die letzten X Blöcke benötigt wurde
        last_block = self.chain[-1]
        block_x_ago = self.chain[-self.adjustment_interval]

        actual_time_taken = last_block.timestamp - block_x_ago.timestamp
        expected_time = self.block_time_target * self.adjustment_interval

        # Debug-Ausgaben zur Anpassung der Schwierigkeit
        print(f"[DEBUG] Schwierigkeit wird überprüft...")

        # Vergleiche tatsächliche Zeit mit der erwarteten Zeit
        if actual_time_taken < expected_time:
            self.difficulty += 1  # Erhöhe die Schwierigkeit
            print(f"[DEBUG] Erhöhe die Schwierigkeit auf {self.difficulty}")

        elif actual_time_taken > expected_time:
            # Verringere die Schwierigkeit, aber nicht unter 1
            self.difficulty = max(1, self.difficulty - 1)
            print(f"[DEBUG] Verringere die Schwierigkeit auf {self.difficulty}")

        print(f"[DEBUG] Zeit für die letzten {self.adjustment_interval} Blöcke: {actual_time_taken:.2f} Sekunden.")

    def get_balance_of_address(self, address: str) -> float:
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
