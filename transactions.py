# Beispiel für Transaktionen (Dummy-Klasse)
class Transaction:
    def __init__(self, sender: str, receiver: str, amount: float):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount


# Beispielnutzung
tx1 = Transaction("Alice", "Bob", 50)
tx2 = Transaction("Bob", "Charlie", 25)
tx3 = Transaction("Charlie", "Dave", 10)
tx4 = Transaction("Dave", "Alice", 5)
