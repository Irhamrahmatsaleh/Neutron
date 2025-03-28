from sqlalchemy import Column, String, Text, Float, ForeignKey
from backend.database.db import Base

class SmartContract(Base):
    __tablename__ = "smart_contracts"

    id = Column(String, primary_key=True)  # ID unik kontrak (bisa kombinasi email + timestamp)
    creator_email = Column(String, ForeignKey("users.email"), nullable=False)
    name = Column(String, nullable=False)
    code = Column(Text, nullable=False)  # isi script kontraknya
    created_at = Column(Float)
    is_active = Column(String, default="true")  # bisa nonaktifkan kontrak

    def to_dict(self):
        return {
            "id": self.id,
            "creator_email": self.creator_email,
            "name": self.name,
            "code": self.code,
            "created_at": self.created_at,
            "is_active": self.is_active
        }
