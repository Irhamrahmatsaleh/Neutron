from backend.models.block import Block
from backend.models.transaction import Transaction
from backend.blockchain.consensus import proof_of_work
from backend.mining.miner import run_miner
from typing import List

class Blockchain:
    def __init__(self):
        self.chain: List[Block] = []
        self.pending_transactions: List[Transaction] = []
        self.difficulty = 4  # jumlah prefix nol untuk hash yang valid
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis_block = Block(index=0, transactions=[], previous_hash="0")
        self.chain.append(genesis_block)

    def get_all_blocks(self):
        return [block.to_dict() for block in self.chain]

    def get_latest_block(self) -> Block:
        return self.chain[-1]

    def add_transaction(self, transaction: Transaction):
        # Validasi sederhana
        if not transaction.sender or not transaction.recipient or not transaction.amount:
            raise ValueError("Transaksi tidak valid.")
        self.pending_transactions.append(transaction)

    def mine_pending_transactions(self, miner_address: str):
        block = Block(
            index=len(self.chain),
            transactions=self.pending_transactions.copy(),
            previous_hash=self.get_latest_block().hash
        )

        # Proof of Work sementara
        result = run_miner(block.to_dict(), self.difficulty)
        if "error" in result:
            raise Exception(result["error"])
        block.hash = result["hash"]
        block.nonce = result["nonce"]

        self.chain.append(block)

        # Hadiah mining
        reward_tx = Transaction(
            sender="NEUTRON_SYSTEM",
            recipient=miner_address,
            amount=1.0,
            signature="SYSTEM"
        )
        self.pending_transactions = [reward_tx]

        return block

    def is_chain_valid(self) -> bool:
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]

            if current.hash != current.calculate_hash():
                return False
            if current.previous_hash != previous.hash:
                return False
        return True

blockchain = Blockchain()
