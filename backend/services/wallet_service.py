import os
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from backend.database.db import SessionLocal
from backend.models.transaction import TransactionRecord
from backend.models.user import User


def generate_key_pair():
    """
    Generate RSA public/private key pair
    """
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    ).decode('utf-8')

    public_key = private_key.public_key()
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    ).decode('utf-8')

    return {"private_key": private_pem, "public_key": public_pem}


def get_balance(email: str) -> float:
    """
    Calculate balance based on transactions from/to user
    """
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.email == email).first()
        if not user:
            raise ValueError("User not found.")

        received = db.query(TransactionRecord).filter(TransactionRecord.recipient == email).all()
        sent = db.query(TransactionRecord).filter(TransactionRecord.sender == email).all()

        total_received = sum(tx.amount for tx in received)
        total_sent = sum(tx.amount for tx in sent)

        return round(total_received - total_sent, 8)
    finally:
        db.close()
