from backend.models.transaction import Transaction
from backend.models.user import User
from backend.database.db import SessionLocal
from backend.services.transaction_service import verify_signature, save_transaction  # Hanya ambil yang dibutuhkan

# Fungsi untuk mengecek saldo pengirim berdasarkan public_key
def check_balance(sender_public_key: str) -> float:
    db = SessionLocal()

    # Normalisasi: ubah "\n" menjadi newline asli
    normalized_sender = sender_public_key.replace("\\n", "\n").strip()

    # Query berdasarkan public_key
    user = db.query(User).filter(User.public_key == normalized_sender).first()

    db.close()
    if user is None:
        raise ValueError("Sender not found.")
    return user.balance

# Fungsi utama untuk memproses transaksi
def process_transaction(tx: Transaction):
    # Normalisasi public key sender (untuk signature)
    normalized_sender = tx.sender.replace("\\n", "\n").strip()

    # Verifikasi tanda tangan
    if verify_signature(normalized_sender, f"{normalized_sender}{tx.recipient}{tx.amount}", tx.signature):
        balance = check_balance(tx.sender)
        if float(balance) < tx.amount:
            raise ValueError("Insufficient balance.")

        saved_tx = save_transaction(tx)
        return {"message": "Transaction successful!", "transaction": saved_tx}
    else:
        return {"message": "Invalid signature."}
