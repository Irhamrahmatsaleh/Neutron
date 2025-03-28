from backend.models.user import User
from backend.database.db import SessionLocal
from backend.services.transaction_service import verify_signature

def verify_token_action_signature(sender_email: str, message: str, signature: str):
    db = SessionLocal()
    try:
        user = db.query(User).filter_by(email=sender_email).first()
        if not user or not user.public_key:
            return False
        return verify_signature(user.public_key, message, signature)
    finally:
        db.close()
