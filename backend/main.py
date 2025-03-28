from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from backend.auth.auth_service import verify_token, sync_user_to_db
from fastapi.responses import FileResponse
from backend.services.transaction_service import sign_transaction, verify_signature
from backend.services.transaction_processing import process_transaction
from backend.models.transaction import Transaction
from backend.blockchain.blockchain import Blockchain
from backend.services.wallet_service import get_balance
from backend.services.wallet_service import generate_key_pair
from backend.services.mining_service import mine_pending_transactions


import os

app = FastAPI()
blockchain = Blockchain()

class User(BaseModel):
    token: str

class TokenRequest(BaseModel):
    token: str

class SignRequest(BaseModel):
    private_key: str
    message: str

class VerifyRequest(BaseModel):
    public_key: str
    message: str
    signature: str

@app.get("/")
async def read_root():
    return {"message": "Welcome to Neutron!"}

@app.get("/favicon.ico")
async def favicon():
    return FileResponse(os.path.join("static", "favicon.ico"))

@app.get("/wallet/create")
async def create_wallet():
    wallet = generate_wallet()
    return wallet

@app.get("/wallet/generate")
async def generate_wallet():
    keys = generate_key_pair()
    return keys


@app.get("/wallet/balance/{email}")
async def get_wallet_balance(email: str):
    try:
        balance = get_balance(email)
        return {"email": email, "balance": balance}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.get("/transaction/pending")
async def get_pending_transactions():
    return [tx.dict() for tx in blockchain.pending_transactions]

@app.get("/mine/{miner_address}")
async def mine_block(miner_address: str):
    new_block = blockchain.mine_pending_transactions(miner_address)
    return {
        "message": "Blok baru berhasil ditambang!",
        "block": new_block.to_dict()
    }

@app.get("/mine/{miner_address}")
async def mine_block(miner_address: str):
    try:
        result = mine_pending_transactions(miner_address)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/auth/verify")
async def verify_user(request: TokenRequest):
    decoded_token = verify_token(request.token)
    if "error" in decoded_token:
        raise HTTPException(status_code=401, detail=decoded_token["error"])

    # 🔁 Sinkronisasi user ke database Neutron
    sync_user_to_db(decoded_token)

    return {"message": "Token is valid", "user": decoded_token}

@app.post("/transaction/sign")
async def sign(sign_req: SignRequest):
    signature = sign_transaction(sign_req.private_key, sign_req.message)
    return {"signature": signature}

@app.post("/transaction/verify")
async def verify(verify_req: VerifyRequest):
    result = verify_signature(verify_req.public_key, verify_req.message, verify_req.signature)
    return {"valid": result}

@app.post("/transaction/new")
async def new_transaction(tx: Transaction):
    # Tambahkan ke mempool (opsional tergantung arsitektur kamu)
    try:
        blockchain.add_transaction(tx)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    # Proses transaksi (verifikasi & simpan ke DB)
    try:
        result = process_transaction(tx)
        if result["message"] == "Transaction successful!":
            tx_data = result["transaction"]
            return {
                "message": result["message"],
                "sender": tx_data.sender,
                "recipient": tx_data.recipient,
                "amount": tx_data.amount,
                "timestamp": str(tx_data.timestamp),
            }
        else:
            raise HTTPException(status_code=400, detail=result["message"])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


