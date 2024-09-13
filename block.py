import hashlib
import time


class Block:
    def __init__(self, index: int, prev_hash: str, transactions: list):
        self.index = index
        self.timestamp = time.time()
        self.transactions = transactions
        self.prev_hash = prev_hash
        self.nonce = 0
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        transactions_str = "".join([tx.__dict__ for tx in self.transactions])
        block_str = f"{self.index}{self.timestamp}{
            transactions_str}{self.prev_hash}{self.nonce}"
        return hashlib.sha256(block_str.encode()).hexdigest()

    # def mine_block(self, difficulty):
    #     target = "0"*difficulty
    #     while self.hash[:difficulty] != target:
    #         self.nonce += 1
    #         self.hash = self.calculate_hash()
