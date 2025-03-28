from sqlalchemy import Column, String, Boolean, Float
from backend.database.db import Base

class User(Base):
    __tablename__ = "users"

    email = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=True)
    is_verified = Column(Boolean, default=False)
    balance = Column(Float, default=0.0)
    public_key = Column(String, unique=True, nullable=True)  # ✅ Tambahkan ini
