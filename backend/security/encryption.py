from cryptography.fernet import Fernet

# Buat kunci rahasia
def generate_key() -> str:
    return Fernet.generate_key().decode()

# Enkripsi data dengan kunci
def encrypt_data(data: str, key: str) -> str:
    f = Fernet(key.encode())
    encrypted = f.encrypt(data.encode())
    return encrypted.decode()

# Dekripsi data
def decrypt_data(token: str, key: str) -> str:
    f = Fernet(key.encode())
    decrypted = f.decrypt(token.encode())
    return decrypted.decode()
