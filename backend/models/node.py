from sqlalchemy import Column, String, Float, ForeignKey
from backend.database.db import Base

class NodePeer(Base):
    __tablename__ = "node_peers"

    id = Column(String, primary_key=True)  # contoh: IP + Port
    owner_email = Column(String, ForeignKey("users.email"), nullable=False)
    ip_address = Column(String, nullable=False)
    port = Column(String, nullable=False)
    reputation = Column(Float, default=0.0)  # bisa kita gunakan untuk penilaian node
    last_seen = Column(Float)

    def to_dict(self):
        return {
            "id": self.id,
            "owner_email": self.owner_email,
            "ip_address": self.ip_address,
            "port": self.port,
            "reputation": self.reputation,
            "last_seen": self.last_seen
        }
