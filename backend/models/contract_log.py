from sqlalchemy import Column, String, Float, Text, ForeignKey
from backend.database.db import Base

class ContractCall(Base):
    __tablename__ = "contract_calls"

    id = Column(String, primary_key=True)
    contract_id = Column(String, ForeignKey("smart_contracts.id"), nullable=False)
    caller_email = Column(String, ForeignKey("users.email"), nullable=False)
    timestamp = Column(Float)
    input_data = Column(Text)
    result = Column(Text)

    def to_dict(self):
        return {
            "id": self.id,
            "contract_id": self.contract_id,
            "caller_email": self.caller_email,
            "timestamp": self.timestamp,
            "input_data": self.input_data,
            "result": self.result
        }
