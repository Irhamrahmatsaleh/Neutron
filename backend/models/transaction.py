import time
from typing import Optional
from pydantic import BaseModel
from sqlalchemy import Column, String, Float, DateTime, Integer
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

# SQLAlchemy model untuk menyimpan transaksi ke dalam database
class TransactionRecord(Base):
    __tablename__ = "transactions"

    # id = Column(String, primary_key=True, index=True)
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    sender = Column(String)
    recipient = Column(String)
    amount = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)
