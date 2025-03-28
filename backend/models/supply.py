from sqlalchemy import Column, Float, String
from backend.database.db import Base

class SupplyLog(Base):
    __tablename__ = "supply_log"

    timestamp = Column(Float, primary_key=True)
    event = Column(String, nullable=False)  # contoh: "mining_reward"
    amount = Column(Float, nullable=False)  # reward yang dikeluarkan
    total_supply = Column(Float, nullable=False)  # supply total setelah reward

    def to_dict(self):
        return {
            "timestamp": self.timestamp,
            "event": self.event,
            "amount": self.amount,
            "total_supply": self.total_supply
        }
