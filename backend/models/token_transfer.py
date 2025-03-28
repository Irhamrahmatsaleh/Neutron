from sqlalchemy import Column, String, Float, ForeignKey
from backend.database.db import Base
from datetime import datetime

class TokenTransfer(Base):
    __tablename__ = "token_transfers"

    id = Column(String, primary_key=True)  # UUID unik
    token_id = Column(String, ForeignKey("token_assets.id"), nullable=False)
    sender = Column(String, ForeignKey("users.email"), nullable=False)
    recipient = Column(String, ForeignKey("users.email"), nullable=False)
    amount = Column(Float, nullable=False)
    timestamp = Column(Float, default=datetime.utcnow().timestamp)
    signature = Column(String, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "token_id": self.token_id,
            "sender": self.sender,
            "recipient": self.recipient,
            "amount": self.amount,
            "timestamp": self.timestamp,
            "signature": self.signature
        }
