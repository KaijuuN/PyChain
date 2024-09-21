from wallet import Wallet

def create_test_wallets(blockchain):
    wallets = [Wallet(blockchain, f"wallet_{i}") for i in range(1, 251)]
    return wallets



# # Beispiel-Wallets (in einem echten System wären sie dynamisch)
# wallets = {
#     'wallet_1': Wallet(blockchain, 'wallet_1'),
#     'wallet_2': Wallet(blockchain, 'wallet_2'),
#     'Kaijuu': Wallet(blockchain, 'Kaijuu'),
#     'Angelina': Wallet(blockchain, 'Angelina'),
# }


# # Initiale Guthaben für die Wallets
# Transaction.credit_wallet(wallets['wallet_1'], 500, transaction_pool, blockchain)
# Transaction.credit_wallet(wallets['wallet_2'], 500, transaction_pool, blockchain)
# Transaction.credit_wallet(wallets['Kaijuu'], 500, transaction_pool, blockchain)
# Transaction.credit_wallet(wallets['Angelina'], 500, transaction_pool, blockchain)

