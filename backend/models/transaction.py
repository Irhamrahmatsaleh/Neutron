import time
from typing import Optional
from pydantic import BaseModel
from sqlalchemy import Column, String, Float, ForeignKey
from backend.database.db import Base
from datetime import datetime

# Pydantic model untuk validasi input dari API
class Transaction(BaseModel):
    sender: str  # Alamat pengirim (public address)
    recipient: str  # Alamat penerima
    amount: float  # Jumlah NTR
    signature: str  # Tanda tangan digital dari pengirim
    timestamp: Optional[float] = time.time()

    def to_dict(self):
        return {
            "sender": self.sender,
            "recipient": self.recipient,
            "amount": self.amount,
            "timestamp": self.timestamp,
        }

class TransactionRecord(Base):
    __tablename__ = "transactions"

    id = Column(String, primary_key=True, index=True)  # Bisa pakai kombinasi hash atau ID unik
    sender = Column(String, ForeignKey("users.email"), nullable=False)
    recipient = Column(String, ForeignKey("users.email"), nullable=False)
    amount = Column(Float, nullable=False)
    timestamp = Column(Float, nullable=False)  # float untuk kompatibel dengan blockchain
    signature = Column(String, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "sender": self.sender,
            "recipient": self.recipient,
            "amount": self.amount,
            "timestamp": self.timestamp,
            "signature": self.signature
        }
