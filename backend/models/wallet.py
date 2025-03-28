from sqlalchemy import Column, String, Float, ForeignKey
from backend.database.db import Base

class Wallet(Base):
    __tablename__ = "wallets"

    address = Column(String, primary_key=True)  # public_key bisa juga
    owner_email = Column(String, ForeignKey("users.email"), nullable=False)
    balance = Column(Float, default=0.0)
    label = Column(String, nullable=True)  # contoh: “dompet utama”, “trading”, dst

    def to_dict(self):
        return {
            "address": self.address,
            "owner_email": self.owner_email,
            "balance": self.balance,
            "label": self.label
        }
