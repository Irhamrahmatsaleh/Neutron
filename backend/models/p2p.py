from sqlalchemy import Column, String, Float, Text
from backend.database.db import Base

class P2PMessage(Base):
    __tablename__ = "p2p_messages"

    id = Column(String, primary_key=True)  # UUID
    sender_node = Column(String)  # public key atau ID node
    receiver_node = Column(String)  # bisa kosong jika broadcast
    message_type = Column(String)  # contoh: "block", "transaction", "ping"
    content = Column(Text)  # JSON message atau isi lainnya
    timestamp = Column(Float)

    def to_dict(self):
        return {
            "id": self.id,
            "sender_node": self.sender_node,
            "receiver_node": self.receiver_node,
            "message_type": self.message_type,
            "content": self.content,
            "timestamp": self.timestamp
        }
