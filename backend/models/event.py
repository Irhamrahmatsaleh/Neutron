from sqlalchemy import Column, String, Float, ForeignKey, Text
from backend.database.db import Base

class EventLog(Base):
    __tablename__ = "event_logs"

    id = Column(String, primary_key=True)  # UUID
    contract_id = Column(String, ForeignKey("smart_contracts.id"), nullable=False)
    event_type = Column(String, nullable=False)  # contoh: "transfer", "vote_cast", dll
    data = Column(Text, nullable=False)  # JSON string (key-value)
    emitted_at = Column(Float)

    def to_dict(self):
        return {
            "id": self.id,
            "contract_id": self.contract_id,
            "event_type": self.event_type,
            "data": self.data,
            "emitted_at": self.emitted_at
        }
