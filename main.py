import random
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
    wallets=[Wallet(blockchain, f"wallet_{i}") for i in range(1,251)]    # Generiert eine Liste mit wallets
    miner_wallet = Wallet(blockchain, "Miner69er")  # miner wallet

    # Definiere die maximale Anzahl von Transaktionen pro Block
    MAX_TRANSACTIONS_PER_BLOCK = 3

    # Befüllt die wallets mit "Startguthaben"
    for wallet in wallets:
        Transaction.credit_wallet(wallet,500,transaction_pool,blockchain)

    # Führe den Mining-Prozess durch, um die Guthaben zu aktivieren
    miner.mine(miner_wallet)
    


    # Generiert "Random" Transactionen zwischen den wallets
    for i in range(0, len(wallets),2):
        transaction_pool.add_transaction(Transaction(wallets[i], wallets[i+1], round(random.uniform(20.0, 138.0),2)), blockchain)

        # Wenn die Anzahl der ausstehenden Transaktionen die Grenze erreicht, mine einen Block
        if len(transaction_pool.pending_transactions) >= MAX_TRANSACTIONS_PER_BLOCK:
            miner.mine(miner_wallet)

    # Mine die ausstehenden Transaktionen (belohne den Miner)
    # miner.mine(miner_wallet)

    # Zeige Informationen über die Blockchain an
    print("\nBlockchain:")
    for block in blockchain.chain:
        print(f"Block {block.index} - Hash: {block.hash} - Previous Hash: {block.prev_hash}")
        print(f"Transactions: {[tx.to_dict() for tx in block.transactions]}")
        print(f"Merkle Root: {block.merkle_root}")
        print("\n")


    print(f"[DEBUG] Balance von Miner69er: {miner_wallet.get_balance(blockchain)}")

    # Überprüfe die Gültigkeit der Blockchain
    if blockchain.is_chain_valid():
        print("\nBlockchain ist gültig.")
    else:
        print("\nBlockchain ist ungültig.")


if __name__ == '__main__':
    main()
