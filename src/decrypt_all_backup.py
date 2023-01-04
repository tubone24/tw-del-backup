import glob
import sys
from encrypt import AESCipher


BACKUP_KEY = sys.argv[1]
FILEPATH = sys.argv[2]


aes = AESCipher(key=BACKUP_KEY)

for file in glob.glob(FILEPATH + "/*.json.enc"):
    aes.decrypt_file(file, delete_raw_file=False)