from backend.database.db import engine, Base, SessionLocal
from backend.models.user import User
from backend.models.transaction import TransactionRecord

# Membuat semua tabel
Base.metadata.create_all(bind=engine)
print("✅ Semua tabel berhasil dibuat!")

# Menambahkan user dummy
db = SessionLocal()

# Cek dulu apakah user sudah ada
existing_user = db.query(User).filter(User.email == "test_sender@example.com").first()

if not existing_user:
    user = User(
        email="test_sender@example.com",
        name="Test Sender",
        is_verified=True,
        balance="1000"  # NTR
    )
    db.add(user)
    db.commit()
    print("✅ User dummy berhasil ditambahkan!")

db.close()
