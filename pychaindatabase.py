import json
import sqlite3
from block import Block
from blockchain import Blockchain
from wallet import Wallet
from cryptography.hazmat.primitives import serialization


def init_db(db='blockchain.db'):
    conn = sqlite3.connect(db)
    c = conn.cursor()
    # Erstelle die Tabelle nur, wenn sie nicht existiert
    c.execute('''CREATE TABLE IF NOT EXISTS blocks
                 (block_index INTEGER, timestamp REAL, transactions TEXT, prev_hash TEXT, nonce INTEGER, merkle_root TEXT, hash TEXT)''')
    conn.commit()
    conn.close()


def save_blockchain(blockchain, db='blockchain.db'):
    conn = sqlite3.connect(db)
    c = conn.cursor()

    for block in blockchain.chain:
        transactions_json = json.dumps([tx.to_dict() for tx in block.transactions])
        c.execute('INSERT INTO blocks (block_index, timestamp, transactions, prev_hash, nonce, merkle_root, hash) VALUES (?, ?, ?, ?, ?, ?, ?)',
                  (block.index, block.timestamp, transactions_json, block.prev_hash, block.nonce, block._merkle_root, block.hash))

    conn.commit()
    conn.close()

def load_blockchain(db='blockchain.db'):
    init_db(db)
    conn = sqlite3.connect(db)
    c = conn.cursor()
    c.execute('SELECT * FROM blocks')
    rows = c.fetchall()

    blockchain = Blockchain()
    for row in rows:
        block = Block(row[0], row[3], json.loads(row[2]))
        block.timestamp = row[1]
        block.nonce = row[4]
        block._merkle_root = row[5]
        block.hash = row[6]
        blockchain.add_block(block)

    conn.close()
    return blockchain


def init_wallet_db(db='wallets.db'):
    conn = sqlite3.connect(db)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS wallets
                 (wallet_address TEXT PRIMARY KEY, public_key TEXT, private_key TEXT, balance REAL)''')
    conn.commit()
    conn.close()



def save_wallet(wallet: Wallet, db: str = 'wallets.db'):
    conn = sqlite3.connect(db)
    c = conn.cursor()
    
    # Serialisiere die private und öffentliche Schlüssel ins PEM-Format
    private_pem = wallet.private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    )
    
    public_pem = wallet.public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    
    # Speichere das Wallet in der Datenbank
    c.execute('INSERT OR REPLACE INTO wallets (wallet_address, public_key, private_key, balance) VALUES (?, ?, ?, ?)',
              (wallet.address, public_pem.decode('utf-8'), private_pem.decode('utf-8'), wallet.get_balance()))
    
    conn.commit()
    conn.close()

def load_wallets(db='wallets.db'):
    init_wallet_db(db)  # Stelle sicher, dass die Tabelle existiert
    conn = sqlite3.connect(db)
    c = conn.cursor()
    c.execute('SELECT * FROM wallets')
    rows = c.fetchall()

    wallets = {}
    for row in rows:
        wallet = Wallet(blockchain=None, address=row[0])  # Erstelle das Wallet ohne Schlüssel
        # Setze die gespeicherten Schlüssel manuell
        wallet.private_key = serialization.load_pem_private_key(
            row[2].encode('utf-8'),
            password=None
        )
        wallet.public_key = serialization.load_pem_public_key(row[1].encode('utf-8'))
        wallets[row[0]] = wallet

    conn.close()
    return wallets
