from backend.blockchain.blockchain import blockchain
from backend.models.transaction import Transaction
from backend.models.block import Block
from backend.services.transaction_service import process_transaction
import time


def mine_pending_transactions(miner_address: str):
    # Ambil semua transaksi di mempool
    pending_txs = blockchain.pending_transactions.copy()
    if not pending_txs:
        return {"message": "No transactions to mine."}

    # Tambahkan reward untuk miner
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
        transactions=[tx.dict() for tx in pending_txs],
        nonce=0
    )

    # Tambahkan ke blockchain
    mined_block = blockchain.mine_block(new_block)
    blockchain.add_block(mined_block)

    # Kosongkan mempool
    blockchain.pending_transactions = []

    return {
        "message": "Block mined successfully!",
        "block_index": mined_block.index,
        "transactions": [tx.dict() for tx in pending_txs],
        "miner_rewarded": miner_address
    }
