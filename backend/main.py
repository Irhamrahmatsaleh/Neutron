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
from backend.database.db import SessionLocal
from backend.models.transaction import TransactionRecord
from backend.models.reward import MiningReward
from backend.models.supply import SupplyLog
from backend.models.token import TokenAsset
from backend.models.token_transfer import TokenTransfer
from backend.models.user import User as UserModel
from backend.services.token_service import verify_token_action_signature
from backend.services.token_service import verify_token_action_signature
import uuid
import time
import os
from fastapi.middleware.cors import CORSMiddleware

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

# Izinkan frontend untuk akses API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
    return {
        "message": "Wallet generated!",
        "private_key": keys["private_key"],
        "public_key": keys["public_key"]
    }

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

@app.get("/blocks")
async def get_all_blocks():
    return {"chain": blockchain.get_all_blocks()}

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

@app.get("/stats")
async def get_stats():
    total_blocks = len(blockchain.chain)
    total_transactions = sum(len(block.transactions) for block in blockchain.chain)
    current_supply = total_transactions * 50  # Jika 1 tx = 1 reward 50 NTR
    return {
        "total_blocks": total_blocks,
        "total_transactions": total_transactions,
        "current_supply": current_supply
    }

@app.get("/transactions/history/{email}")
async def get_transaction_history(email: str):
    db = SessionLocal()
    try:
        sent = db.query(TransactionRecord).filter(TransactionRecord.sender == email).all()
        received = db.query(TransactionRecord).filter(TransactionRecord.recipient == email).all()

        sent_list = [tx.to_dict() for tx in sent]
        received_list = [tx.to_dict() for tx in received]

        return {
            "email": email,
            "sent": sent_list,
            "received": received_list,
            "total_sent": len(sent_list),
            "total_received": len(received_list)
        }
    finally:
        db.close()

@app.get("/rewards/{email}")
async def get_rewards(email: str):
    db = SessionLocal()
    try:
        rewards = db.query(MiningReward).filter(MiningReward.miner_email == email).all()
        return {
            "miner": email,
            "total_reward": sum(r.amount for r in rewards),
            "history": [r.to_dict() for r in rewards]
        }
    finally:
        db.close()

@app.get("/supply/total")
async def get_total_supply():
    db = SessionLocal()
    try:
        latest = db.query(SupplyLog).order_by(SupplyLog.timestamp.desc()).first()
        return {"total_supply": latest.total_supply if latest else 0.0}
    finally:
        db.close()

@app.post("/token/create")
async def create_token(data: dict):
    db = SessionLocal()
    try:
        # Verifikasi signature
        message = f"{data['creator_email']}|{data['name']}|{data['symbol']}|{data['total_supply']}"
        valid = verify_token_action_signature(
            sender_email=data["creator_email"],
            message=message,
            signature=data["signature"]
        )
        if not valid:
          raise HTTPException(status_code=403, detail="Invalid signature for token creation")

        token = TokenAsset(
            id=str(uuid.uuid4()),
            creator_email=data["creator_email"],
            name=data["name"],
            symbol=data["symbol"],
            total_supply=data["total_supply"],
            decimal=data.get("decimal", 8),
            created_at=time.time(),
            is_active=True
        )
        db.add(token)
        db.commit()
        return {"message": "Token created!", "token": token.to_dict()}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        db.close()

@app.post("/token/transfer")
async def transfer_token(data: dict):
    db = SessionLocal()
    try:
        token = db.query(TokenAsset).filter_by(id=data["token_id"]).first()
        if not token or not token.is_active:
            raise HTTPException(status_code=404, detail="Token not found or inactive.")

        sender = db.query(UserModel).filter_by(email=data["sender"]).first()
        recipient = db.query(UserModel).filter_by(email=data["recipient"]).first()

                # 🧠 Verifikasi Signature (sebelum lanjut)
        valid = verify_token_action_signature(
            sender_email=data["sender"],
            message=f"{data['token_id']}|{data['recipient']}|{data['amount']}",
            signature=data["signature"]
        )
        if not valid:
            raise HTTPException(status_code=403, detail="Invalid signature")

        if not sender or not recipient:
            raise HTTPException(status_code=404, detail="Sender or recipient not found.")

        # Sementara, kita asumsikan tidak ada saldo (future work: saldo wallet token)
        transfer = TokenTransfer(
            id=str(uuid.uuid4()),
            token_id=token.id,
            sender=data["sender"],
            recipient=data["recipient"],
            amount=data["amount"],
            timestamp=time.time(),
            signature=data["signature"]
        )
        db.add(transfer)
        db.commit()
        return {"message": "Token transfer recorded!", "transfer": transfer.to_dict()}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        db.close()

@app.post("/dev/create_user")
async def dev_create_user(data: dict):
    db = SessionLocal()
    try:
        # ✅ Cek apakah user sudah ada
        existing = db.query(UserModel).filter_by(email=data["email"]).first()
        if existing:
            return {"message": "User already exists!", "user": existing.to_dict()}

        # 🔨 Kalau belum ada, buat user baru
        user = UserModel(
            email=data["email"],
            public_key=data["public_key"]
        )
        db.add(user)
        db.commit()
        return {"message": "User created!", "user": user.to_dict()}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        db.close()

@app.get("/token/{token_id}/transfers")
async def get_token_transfers(token_id: str):
    db = SessionLocal()
    try:
        transfers = db.query(TokenTransfer).filter_by(token_id=token_id).all()
        return {
            "token_id": token_id,
            "total": len(transfers),
            "transfers": [t.to_dict() for t in transfers]
        }
    finally:
        db.close()


@app.get("/token/list")
async def list_tokens():
    db = SessionLocal()
    try:
        tokens = db.query(TokenAsset).all()
        return {
            "total": len(tokens),
            "tokens": [t.to_dict() for t in tokens]
        }
    finally:
        db.close()

@app.get("/token/{token_id}")
async def get_token_detail(token_id: str):
    db = SessionLocal()
    try:
        token = db.query(TokenAsset).filter_by(id=token_id).first()
        if not token:
            raise HTTPException(status_code=404, detail="Token not found")
        return token.to_dict()
    finally:
        db.close()


@app.get("/token/{token_id}/balance/{email}")
async def get_token_balance(token_id: str, email: str):
    db = SessionLocal()
    try:
        sent = db.query(TokenTransfer).filter_by(sender=email, token_id=token_id).all()
        received = db.query(TokenTransfer).filter_by(recipient=email, token_id=token_id).all()

        total_sent = sum(t.amount for t in sent)
        total_received = sum(t.amount for t in received)
        balance = total_received - total_sent

        return {
            "email": email,
            "token_id": token_id,
            "balance": balance,
            "total_sent": total_sent,
            "total_received": total_received
        }
    finally:
        db.close()

@app.post("/token/burn")
async def burn_token(data: dict):
    db = SessionLocal()
    try:
        token = db.query(TokenAsset).filter_by(id=data["token_id"]).first()
        if not token or not token.is_active:
            raise HTTPException(status_code=404, detail="Token not found or inactive.")

        sender = db.query(UserModel).filter_by(email=data["sender"]).first()
        if not sender:
            raise HTTPException(status_code=404, detail="Sender not found.")

        # Hitung saldo token
        sent = db.query(TokenTransfer).filter_by(sender=data["sender"], token_id=data["token_id"]).all()
        received = db.query(TokenTransfer).filter_by(recipient=data["sender"], token_id=data["token_id"]).all()
        balance = sum(t.amount for t in received) - sum(t.amount for t in sent)

        if balance < data["amount"]:
            raise HTTPException(status_code=400, detail="Insufficient balance to burn.")

        # Kurangi total supply
        token.total_supply -= data["amount"]

        # Simpan transaksi burn (tujuannya ke null address)
        burn_tx = TokenTransfer(
            id=str(uuid.uuid4()),
            token_id=token.id,
            sender=data["sender"],
            recipient="null@burn",
            amount=data["amount"],
            timestamp=time.time(),
            signature=data["signature"]
        )

        db.add(burn_tx)
        db.commit()
        return {"message": "Token burned!", "burn_transaction": burn_tx.to_dict(), "new_supply": token.total_supply}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        db.close()
