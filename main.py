from miner import Miner
from transactionpool import TransactionPool
from transactions import Transaction
from blockchain import Blockchain
from wallet import Wallet


def main():
    # Initialisiere
    blockchain = Blockchain()
    transaction_pool = TransactionPool()
    miner = Miner(blockchain, transaction_pool)

    # Wallets erstellen
    alice_wallet = Wallet(blockchain, "Alice")
    bob_wallet = Wallet(blockchain, "Bob")
    miner_wallet = Wallet(blockchain, "Miner69er")

    # Beispiel-Transaktionen hinzufügen
    # transaction_pool.add_transaction(alice_wallet, bob_wallet, 50, blockchain)
    transaction_pool.add_transaction(Transaction(
        alice_wallet, bob_wallet, 50), blockchain)
    transaction_pool.add_transaction(Transaction(
        bob_wallet, alice_wallet, 25), blockchain)

    # Mine die ausstehenden Transaktionen (belohne den Miner)
    miner.mine(miner_wallet)

    # Zeige Informationen über die Blockchain an
    print("\nBlockchain:")
    for block in blockchain.chain:
        print(
            f"Block {block.index} - Hash: {block.hash} - Previous Hash: {block.prev_hash}")
        print(f"Transactions: {[tx.__dict__ for tx in block.transactions]}")
        print(f"Merkle Root: {block.merkle_root}")
        print("\n")

    # Kontostände abfragen
    print(f"Balance von Alice: {alice_wallet.get_balance()}")
    print(f"Balance von Bob: {bob_wallet.get_balance()}")
    print(f"Balance von Miner69er: {miner_wallet.get_balance()}")

    # Überprüfe die Gültigkeit der Blockchain
    if blockchain.is_chain_valid():
        print("\nBlockchain ist gültig.")
    else:
        print("\nBlockchain ist ungültig.")


if __name__ == '__main__':
    main()
