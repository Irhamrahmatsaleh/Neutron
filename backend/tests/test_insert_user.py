from sqlalchemy.exc import IntegrityError
from backend.database.db import SessionLocal
from backend.models.user import User

def insert_user(email: str, public_key_pem: str):
    db = SessionLocal()
    try:
        user = User(
            email=email,
            name=None,
            is_verified=False,
            balance=0.0,
        )
        setattr(user, "public_key", public_key_pem)

        db.add(user)
        db.commit()
        print("✅ Public key berhasil ditambahkan ke database.")
    except IntegrityError as e:
        print("⚠️ Gagal menambahkan user. Mungkin user sudah ada.")
        db.rollback()
    except Exception as e:
        print("❌ Error:", e)
        db.rollback()
    finally:
        db.close()

# Contoh penggunaan
email = "alice@example.com"
public_key = """-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAhoDwsfqdI9LX/F5YS4vJ
t71Nkt5xtpv0ApfEKAyiDUroTGFjtIRCpY1j0GxL/Fc2gHjWNrh4X4nWQ+VxUFMS
pCoPkT3XlZuE77OzTeglGYnEFdYqlkczixMidDyDJgTLIkPesPW1yrhMh+muYHBU
cQD0CMA/kaEbhcJCYd8OPDlEH2qGwkmsP9NxbZAMRsWVw1rgdLPqUn+gH3E4b1ai
QZSbgA3PDvYiMBCTR2SYkYSatJJxOAYaAU7EVV6iAxP781S6KNSiaKE8XtSy8HS/
zdndI2fg5IopPGBXkycThkN+b2P2B10IMY736YbkmH95qFdHN/MDKbaKIJSJP0Ld
wQIDAQAB
-----END PUBLIC KEY-----"""

insert_user(email, public_key)
