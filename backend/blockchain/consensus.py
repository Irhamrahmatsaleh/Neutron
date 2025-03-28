def proof_of_work(block, difficulty: int) -> str:
    block.nonce = 0
    computed_hash = block.calculate_hash()
    while not computed_hash.startswith("0" * difficulty):
        block.nonce += 1
        computed_hash = block.calculate_hash()
    return computed_hash

def is_valid_proof(block, difficulty: int) -> bool:
    return block.hash.startswith("0" * difficulty) and block.hash == block.calculate_hash()
