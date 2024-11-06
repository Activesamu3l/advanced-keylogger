from cryptography.fernet import Fernet

# Generate a new, random encryption key using Fernet
key = Fernet.generate_key()

# Store the key securely in the "encryption_key.txt" file
with open("encryption_key.txt", 'wb') as f:
    f.write(key)