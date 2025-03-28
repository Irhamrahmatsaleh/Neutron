from backend.services.transaction_service import save_bulk_transactions
from backend.blockchain.blockchain import blockchain
from backend.models.transaction import Transaction
from backend.models.block import Block
from backend.models.block import BlockRecord
from backend.database.db import SessionLocal
from backend.models.reward import MiningReward
from datetime import datetime
from backend.models.supply import SupplyLog
import time
import json

def mine_pending_transactions(miner_address: str):
    pending_txs = blockchain.pending_transactions.copy()
    if not pending_txs:
        return {"message": "No transactions to mine."}

    reward_tx = Transaction(
        sender="SYSTEM",
        recipient=miner_address,
        amount=50.0,
        signature="SYSTEM_REWARD"
    )
    pending_txs.append(reward_tx)

    # Buat block baru
    new_block = Block(
        index=len(blockchain.chain),
        previous_hash=blockchain.get_last_block().hash,
        timestamp=time.time(),
        transactions=[tx.dict() for tx in pending_txs if tx.sender != "SYSTEM"],
        nonce=0
    )

    # Tambahkan ke blockchain
    mined_block = blockchain.mine_block(new_block)
    blockchain.add_block(mined_block)
    save_block_to_db(mined_block)  # ✅ Simpan block
    save_mining_reward(miner_address, 50.0)
    log_supply_change("mining_reward", 50.0)
    save_bulk_transactions(mined_block.transactions)

    blockchain.pending_transactions = []

    return {
        "message": "Block mined successfully!",
        "block_index": mined_block.index,
        "transactions": [tx.dict() for tx in pending_txs],
        "miner_rewarded": miner_address
    }

def save_block_to_db(block):
    db = SessionLocal()
    try:
        record = BlockRecord(
            index=block.index,
            timestamp=block.timestamp,
            previous_hash=block.previous_hash,
            nonce=block.nonce,
            hash=block.hash,
            transactions=json.dumps(block.transactions)  # Konversi list transaksi ke JSON string
        )
        db.add(record)
        db.commit()
    except Exception as e:
        print(f"❌ Gagal simpan block ke DB: {e}")
        db.rollback()
    finally:
        db.close()

def save_mining_reward(miner_email: str, amount: float):
    db = SessionLocal()
    try:
        reward = MiningReward(
            id=f"{miner_email}-{datetime.utcnow().timestamp()}",
            miner_email=miner_email,
            amount=amount,
            timestamp=datetime.utcnow().timestamp()
        )
        db.add(reward)
        db.commit()
    except Exception as e:
        print(f"❌ Gagal menyimpan reward: {e}")
        db.rollback()
    finally:
        db.close()

def log_supply_change(event: str, amount: float):
    db = SessionLocal()
    try:
        # Hitung total supply sekarang dari tabel supply_log
        current_total = db.query(SupplyLog).with_entities(SupplyLog.total_supply).order_by(SupplyLog.timestamp.desc()).first()
        total = (current_total[0] if current_total else 0.0) + amount

        supply = SupplyLog(
            timestamp=time.time(),
            event=event,
            amount=amount,
            total_supply=total
        )
        db.add(supply)
        db.commit()
    except Exception as e:
        print(f"❌ Gagal log suplai: {e}")
        db.rollback()
    finally:
        db.close()
