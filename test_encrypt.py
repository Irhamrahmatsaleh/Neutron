from backend.security.encryption import generate_key, encrypt_data, decrypt_data

key = generate_key()
print("KEY:", key)

secret = encrypt_data("rahasia", key)
print("ENCRYPTED:", secret)

original = decrypt_data(secret, key)
print("DECRYPTED:", original)
