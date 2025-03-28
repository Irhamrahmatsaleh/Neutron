import firebase_admin
from firebase_admin import credentials, auth
from backend.database.db import SessionLocal
from backend.models.user import User

# Menggunakan file firebase_key.json
cred = credentials.Certificate('backend/auth/firebase_key.json')
firebase_admin.initialize_app(cred)

def verify_token(id_token):
    try:
        decoded_token = auth.verify_id_token(id_token)
        return decoded_token
    except Exception as e:
        return {"error": str(e)}


def sync_user_to_db(decoded_token: dict):
    email = decoded_token.get("email")
    name = decoded_token.get("name", "Anonymous")

    db = SessionLocal()
    try:
        user = db.query(User).filter(User.email == email).first()
        if not user:
            new_user = User(
                email=email,
                name=name,
                is_verified=True,
                balance=0.0
            )
            db.add(new_user)
            db.commit()
            print(f"✅ New user created: {email}")
        else:
            print(f"ℹ️ User already exists: {email}")
    except Exception as e:
        print(f"⚠️ Failed to sync user: {str(e)}")
        db.rollback()
    finally:
        db.close()
