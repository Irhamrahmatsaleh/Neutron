from backend.models.transaction import Transaction, TransactionRecord
from backend.database.db import SessionLocal
from backend.models.user import User
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization
from backend.models.transaction import TransactionRecord


def sign_transaction(private_key_pem: str, message: str) -> str:
    private_key = serialization.load_pem_private_key(
        private_key_pem.encode('utf-8'),
        password=None,
    )
    signature = private_key.sign(
        message.encode('utf-8'),
        padding.PKCS1v15(),
        hashes.SHA256()
    )
    return signature.hex()


def verify_signature(public_key_pem: str, message: str, signature_hex: str) -> bool:
    public_key = serialization.load_pem_public_key(
        public_key_pem.encode('utf-8'),
    )
    try:
        public_key.verify(
            bytes.fromhex(signature_hex),
            message.encode('utf-8'),
            padding.PKCS1v15(),
            hashes.SHA256()
        )
        return True
    except Exception:
        return False


def save_transaction(tx: Transaction):
    db = SessionLocal()
    try:
        # Ambil data pengguna dari database
        sender = db.query(User).filter(User.email == tx.sender).first()
        recipient = db.query(User).filter(User.email == tx.recipient).first()

        if not sender:
            raise ValueError("Sender not found.")
        if not recipient:
            raise ValueError("Recipient not found.")
        if sender.balance < tx.amount:
            raise ValueError("Insufficient balance.")

        # Buat dan simpan transaksi
        db_tx = TransactionRecord(
            id=f"{tx.sender}-{tx.recipient}-{tx.timestamp}",
            sender=tx.sender,
            recipient=tx.recipient,
            amount=tx.amount,
            timestamp=tx.timestamp
        )
        db.add(db_tx)

        # Update saldo
        sender.balance -= tx.amount
        recipient.balance += tx.amount

        db.commit()
        db.refresh(db_tx)
        return db_tx

    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()

def save_bulk_transactions(transactions: list):
    db = SessionLocal()
    try:
        for tx in transactions:
            if tx["sender"] != "SYSTEM":  # Reward tidak disimpan sebagai tx biasa
                record = TransactionRecord(
                    id=f'{tx["sender"]}-{tx["recipient"]}-{tx["timestamp"]}',
                    sender=tx["sender"],
                    recipient=tx["recipient"],
                    amount=tx["amount"],
                    timestamp=tx["timestamp"],
                    signature=tx["signature"]
                )
                db.add(record)
        db.commit()
    except Exception as e:
        print(f"❌ Gagal simpan transaksi bulk: {e}")
        db.rollback()
    finally:
        db.close()


def process_transaction(tx: Transaction):
    message = f"{tx.sender}{tx.recipient}{tx.amount}"
    if verify_signature(tx.sender, message, tx.signature):
        saved_tx = save_transaction(tx)
        return {"message": "Transaction successful!", "transaction": saved_tx}
    else:
        return {"message": "Invalid signature."}
