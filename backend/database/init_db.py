from backend.database.db import engine, Base
from backend.models.user import User
from backend.models.transaction import TransactionRecord

User.metadata.create_all(bind=engine)
TransactionRecord.metadata.create_all(bind=engine)

# ⛏️ Buat tabel di database
print("🔨 Creating tables in the database...")
Base.metadata.create_all(bind=engine)
print("✅ Tables created successfully.")
