import os
from encrypt import AESCipher
BACKUP_KEY = os.getenv("BACKUP_KEY")

aes = AESCipher(key=BACKUP_KEY)

aes.decrypt_file("backup.json.enc", delete_raw_file=False)
