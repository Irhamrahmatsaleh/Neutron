from sqlalchemy import Column, String, Text
from backend.database.db import Base

class ChainSetting(Base):
    __tablename__ = "chain_settings"

    key = Column(String, primary_key=True)
    value = Column(Text, nullable=False)
    description = Column(Text)

    def to_dict(self):
        return {
            "key": self.key,
            "value": self.value,
            "description": self.description
        }
