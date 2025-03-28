from sqlalchemy import Column, String, Text, Float, ForeignKey
from backend.database.db import Base

class ContractStorage(Base):
    __tablename__ = "contracts_storage"

    id = Column(String, primary_key=True)  # bisa UUID
    contract_id = Column(String, ForeignKey("smart_contracts.id"), nullable=False)
    key = Column(String, nullable=False)     # nama variabel
    value = Column(Text, nullable=False)     # isi variabel
    updated_at = Column(Float)

    def to_dict(self):
        return {
            "id": self.id,
            "contract_id": self.contract_id,
            "key": self.key,
            "value": self.value,
            "updated_at": self.updated_at
        }
