from sqlalchemy import Column, String, Float, ForeignKey
from backend.database.db import Base

class SessionToken(Base):
    __tablename__ = "session_tokens"

    token = Column(String, primary_key=True)
    email = Column(String, ForeignKey("users.email"), nullable=False)
    created_at = Column(Float)
    expires_at = Column(Float)

    def to_dict(self):
        return {
            "token": self.token,
            "email": self.email,
            "created_at": self.created_at,
            "expires_at": self.expires_at
        }
