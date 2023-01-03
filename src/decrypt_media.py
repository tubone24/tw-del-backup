from encrypt import AESCipher
BACKUP_KEY = sys.argv[1]
FILEPATH = sys.argv[2]

aes = AESCipher(key=BACKUP_KEY)
aes.decrypt_bytes(FILEPATH + ".enc", delete_raw_file=True)