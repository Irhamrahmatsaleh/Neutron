from sqlalchemy import Column, String, Float
from backend.database.db import Base

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(String, primary_key=True)  # UUID
    email = Column(String)  # bisa None jika sistem
    action = Column(String, nullable=False)  # contoh: "login", "create_wallet"
    timestamp = Column(Float)
    details = Column(String)  # Ganti dari "metadata" → "details"

    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "action": self.action,
            "timestamp": self.timestamp,
            "details": self.details
        }
