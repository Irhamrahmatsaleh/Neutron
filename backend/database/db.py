from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

# ⛳️ Load environment variables dari file .env
load_dotenv()

# 🌐 Ambil DATABASE_URL dari .env, fallback ke default lokal
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:root@localhost:5432/postgres")

# 🏗️ Buat SQLAlchemy Engine
engine = create_engine(DATABASE_URL)

# 🧵 Buat session lokal (untuk komunikasi ke DB)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 🧬 Base class untuk model-model SQLAlchemy
Base = declarative_base()
