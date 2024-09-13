
from block import Block
from transactions import Transaction


def main():
    pass


if __name__ == '__main__':
    # Beispielnutzung
    tx1 = Transaction("Alice", "Bob", 50)
    tx2 = Transaction("Bob", "Charlie", 25)
    tx3 = Transaction("Charlie", "Dave", 10)
    tx4 = Transaction("Dave", "Alice", 5)

    block = Block(1, "0" * 64, [tx1, tx2, tx3, tx4])

    # Blockinformationen ausgeben
    print(f"Block-Hash: {block.hash}")
    print(f"Merkle-Root: {block.merkle_root}")
