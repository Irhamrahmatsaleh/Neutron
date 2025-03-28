from sqlalchemy import Column, String, Boolean, Float, Text
from backend.database.db import Base

class User(Base):
    __tablename__ = "users"

    # email = Column(String, primary_key=True, index=True)
    email = Column(String, primary_key=True)
    name = Column(String, nullable=True)
    is_verified = Column(Boolean, default=False)
    balance = Column(Float, default=0.0)
    # public_key = Column(String, unique=True, nullable=True)
    public_key = Column(Text)

    def to_dict(self):
        return {
            "email": self.email,
            "public_key": self.public_key
        }
