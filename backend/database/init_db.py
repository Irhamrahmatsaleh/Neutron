from backend.database.db import engine, Base

# 🧠 Impor semua model yang ingin dimigrasi
from backend.models.user import User
from backend.models.transaction import TransactionRecord
from backend.models.block import BlockRecord
from backend.models.reward import MiningReward
from backend.models.node import NodePeer
from backend.models.contract import SmartContract
from backend.models.contract_log import ContractCall
from backend.models.supply import SupplyLog
from backend.models.wallet import Wallet
from backend.models.session import SessionToken
from backend.models.audit import AuditLog
from backend.models.storage import ContractStorage
from backend.models.event import EventLog
from backend.models.p2p import P2PMessage
from backend.models.settings import ChainSetting
from backend.models.token import TokenAsset
from backend.models.token_transfer import TokenTransfer





# 🔨 Buat tabel-tabel di database
print("🔨 Creating tables in the database...")
Base.metadata.create_all(bind=engine)
print("✅ Tables created successfully.")
