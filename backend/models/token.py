from sqlalchemy import Column, String, Float, Integer, Boolean, ForeignKey
from backend.database.db import Base
from datetime import datetime

class TokenAsset(Base):
    __tablename__ = "token_assets"

    id = Column(String, primary_key=True)  # UUID
    creator_email = Column(String, ForeignKey("users.email"), nullable=False)
    name = Column(String, nullable=False)  # Contoh: NeutronToken
    symbol = Column(String, nullable=False)  # Contoh: NTRT
    total_supply = Column(Float, nullable=False)
    decimal = Column(Integer, default=8)
    created_at = Column(Float, default=datetime.utcnow().timestamp)
    is_active = Column(Boolean, default=True)

    def to_dict(self):
        return {
            "id": self.id,
            "creator_email": self.creator_email,
            "name": self.name,
            "symbol": self.symbol,
            "total_supply": self.total_supply,
            "decimal": self.decimal,
            "created_at": self.created_at,
            "is_active": self.is_active
        }
