import subprocess
import json
import os
import sys

# Path ke miner.exe
EXE_PATH = os.path.abspath("backend/blockchain/mining/build/Debug/miner.exe")

def run_miner(block_data: dict, difficulty: int) -> dict:
    try:
        # Ubah data blok ke string JSON
        json_data = json.dumps(block_data)

        # Jalankan subprocess ke miner.exe
        process = subprocess.Popen(
            [EXE_PATH],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        # Kirim data & difficulty ke stdin
        stdout, stderr = process.communicate(input=f"{json_data}\n{difficulty}")

        if process.returncode != 0:
            raise Exception(f"Mining Error: {stderr.strip()}")

        # Pisahkan hash dan nonce dari output stdout
        hash_str, nonce_str = stdout.strip().split()
        return {"hash": hash_str, "nonce": int(nonce_str)}

    except Exception as e:
        return {"error": str(e)}
