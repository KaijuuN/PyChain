
from block import Block


class Blockchain:
    def __init__(self):
        self.chain = []  # Initialisiert eine leere liste
        self.pendings_transactions = []  # Initialisiert eine leere liste

    def create_genesis_block(self):
        if len(self.chain) != 0:
            return

        genesis_block = Block(0, "GENESIS BLOCK", [])
