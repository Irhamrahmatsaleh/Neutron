# 🪐 Neutron: The Future of Cosmic Currency

Welcome to **Neutron**, an interstellar cryptocurrency built from the void of space with Python precision.
A 100% functional clone of Bitcoin — **with a finite total supply of 23,000,000 Neutron (NTR)** and **each Neutron divisible into 100,000,000 Chip**.

> "Born in the stars. Forged in code. Powered by belief."

---

## 🌌 Overview

**Neutron** is a fully open-source cryptocurrency project that simulates the core mechanics of Bitcoin, redesigned for developers and learners. It includes:

- 🔐 Wallet system with public/private keys
- 🛰️ Google Auth (Firebase)
- 🌐 React frontend
- 🚀 FastAPI backend
- 💾 PostgreSQL integration
- 🧠 Blockchain logic with mining & halving (coming soon)

> NOTE: This project is ideal for developers who want to **learn how Bitcoin works** under the hood — from transaction logic to blockchain simulation.

---

## 🛠 Tech Stack

| Layer          | Stack                                  |
| -------------- | -------------------------------------- |
| Backend        | Python, FastAPI, SQLAlchemy            |
| Database       | PostgreSQL                             |
| Frontend       | React.js + Vite                        |
| Authentication | Firebase Google Auth                   |
| Hosting        | Railway / Vercel / Firebase (optional) |

---

## 🧩 Folder Structure

```
neutron/
│
├── backend/
│   ├── auth/               # Firebase Auth logic
│   ├── db/                 # PostgreSQL connection & models
│   ├── core/               # Blockchain engine (coming soon)
│   ├── test_insert_user.py # Test inserting user with public key
│   └── main.py             # FastAPI entrypoint
│
├── frontend/
│   └── ...                 # React components & routes
│
├── firebase_key.json       # Firebase service account credentials
├── .env                    # Backend environment config
├── .env (frontend)         # Frontend Firebase env config
└── README.md               # This file
```

> NOTE: Keep `firebase_key.json` and `.env` safe and NEVER upload them to public repositories!

---

## ⚙️ Backend Setup

### 1. Create virtual environment

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Create `.env` file

```env
EMAIL_ADDRESS=your_email@gmail.com
EMAIL_PASSWORD=your_app_password
FIREBASE_CREDENTIALS=backend/auth/firebase_key.json
DATABASE_URL=postgresql://postgres:root@localhost:5432/postgres
```

> NOTE: Replace values with your actual credentials. Use **App Password** for Gmail.

### 4. Run the server

```bash
uvicorn main:app --reload
```

---

## 🌐 Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

### Create `.env` file in `frontend/`

```env
VITE_FIREBASE_API_KEY=your_api_key
VITE_FIREBASE_AUTH_DOMAIN=your_project.firebaseapp.com
VITE_FIREBASE_PROJECT_ID=your_project
VITE_FIREBASE_STORAGE_BUCKET=your_project.appspot.com
VITE_FIREBASE_MESSAGING_SENDER_ID=your_sender_id
VITE_FIREBASE_APP_ID=your_app_id
```

> NOTE: All of this can be copied from your Firebase project dashboard → Project Settings.

---

## 🔐 Test User Wallet Insertion

You can test inserting a user with a generated wallet:

```bash
python test_insert_user.py
```

> NOTE: This script will auto-generate a public/private key pair and insert the public key into the database.

---

## 🚧 Features in Progress

- [x] Firebase Auth + Login/Signup
- [x] PostgreSQL integration for user wallets
- [ ] Blockchain & mining logic
- [ ] Wallet balance & transaction system
- [ ] Neutron (NTR) Halving Algorithm
- [ ] Complete wallet dashboard UI
- [ ] Real-time block explorer
- [ ] Global deployment & optimization

---

## 🧬 Tokenomics

- Total Supply: **23,000,000 NTR**
- 1 NTR = **100,000,000 Chip**
- Algorithm: Proof-of-Work (PoW) Simulation (Coming Soon)
- Reward Halving: Every fixed interval (Inspired by Bitcoin)

> NOTE: These numbers are customizable if you'd like to simulate different crypto behaviors.

---

## 👽 Credits

Made with ❤️ by developers who dream in Python and code among the stars.

For collaboration, contact:
📧 **irhamsaleh904@gmail.com**

---

## 📄 License

This project is licensed under the MIT License.
You are free to fork, learn, and build your own galaxy of decentralized applications.

> NOTE: Star this repo if you believe in **open-source, decentralized freedom**.
