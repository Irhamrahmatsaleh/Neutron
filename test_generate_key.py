from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization

# 1. Generate Private Key
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
)

# 2. Generate Public Key dari Private Key
public_key = private_key.public_key()

# 3. Serialize ke format PEM (agar bisa dikirim via API)
private_pem = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.TraditionalOpenSSL,
    encryption_algorithm=serialization.NoEncryption()
)

public_pem = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)

# 4. Tampilkan hasil kunci
print("🔐 PRIVATE KEY PEM:\n", private_pem.decode())
print("🔑 PUBLIC KEY PEM:\n", public_pem.decode())

# 5. Data yang akan ditandatangani (contoh)
sender = public_pem.decode()
recipient = "bob@example.com"
amount = 10.5
message = f"{sender}{recipient}{amount}"

# 6. Tanda Tangani Pesan
signature = private_key.sign(
    message.encode(),
    padding.PKCS1v15(),
    hashes.SHA256()
)

print("🖋️ SIGNATURE HEX:\n", signature.hex())
# Cetak ulang string message yang ditandatangani
print("\n📦 MESSAGE YANG DITANDATANGANI:")
print(message)
print("\n✅ COPY PASTE INI KE THUNDER CLIENT (Field sender):")
print(public_pem.decode().replace("\n", "\\n"))


# 🔁 Format JSON final untuk Thunder Client (biar tinggal copy langsung)
formatted_sender = public_pem.decode().replace("\n", "\\n")

print("\n🎯 JSON UNTUK THUNDER CLIENT:")
print("{")
print(f'  "sender": "{formatted_sender}",')
print('  "recipient": "bob@example.com",')
print('  "amount": 10.5,')
print(f'  "signature": "{signature.hex()}"')
print("}")
