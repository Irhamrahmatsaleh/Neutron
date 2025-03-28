from sqlalchemy import Column, String, Float, ForeignKey
from backend.database.db import Base

class MiningReward(Base):
    __tablename__ = "rewards"

    id = Column(String, primary_key=True)  # Bisa kombinasi hash atau miner+timestamp
    miner_email = Column(String, ForeignKey("users.email"), nullable=False)
    amount = Column(Float, nullable=False)
    timestamp = Column(Float, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "miner_email": self.miner_email,
            "amount": self.amount,
            "timestamp": self.timestamp
        }
