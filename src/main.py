import tweepy
import json
import toml
import os
from datetime import datetime, timedelta
from encrypt import AESCipher
from save_media import save_tweet_media
CONSUMER_KEY = os.getenv("CONSUMER_KEY")
CONSUMER_SECRET = os.getenv("CONSUMER_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_SECRET = os.getenv("ACCESS_SECRET")
BACKUP_KEY = os.getenv("BACKUP_KEY")
BEFORE_DAYS = int(os.getenv("BEFORE_DAYS", "7"))
GITHUB_SERVER_URL = os.getenv("GITHUB_SERVER_URL")
GITHUB_REPOSITORY = os.getenv("GITHUB_REPOSITORY")
GITHUB_RUN_ID = os.getenv("GITHUB_RUN_ID")
GITHUB_ACTIONS_URL = f"{GITHUB_SERVER_URL}/{GITHUB_REPOSITORY}/actions/runs/{GITHUB_RUN_ID}"
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth)
account = api.me()
tweets = tweepy.Cursor(api.user_timeline, id=account.id).items(100000)
aes = AESCipher(key=BACKUP_KEY)
backup = []

config = toml.load(open("config.toml"))

try:
    aes.decrypt_file("backup.json.enc", delete_raw_file=True)
    with open("backup.json", "r+") as f:
        backup = json.loads(f.read())
except FileNotFoundError:
    pass
delete_count = 0
first_tweet_text = ""
for tweet in tweets:
    if tweet.id_str in config["delete_ignore"]["ids"]:
        print(f"{tweet.id_str} is delete ignore tweet")
        continue
    first_tweet_text = tweet.text
    before_two_days = datetime.now() - timedelta(days=BEFORE_DAYS)
    if tweet.created_at < before_two_days:
        backup.append(tweet._json)
        print(tweet.created_at, tweet.id_str)
        save_tweet_media(tweet._json, BACKUP_KEY)
        api.destroy_status(tweet.id)
        delete_count += 1

with open("backup.json", "w") as f:
    f.write(json.dumps(backup))
aes.encrypt_file("backup.json", delete_raw_file=True)

if delete_count != 0:
    if delete_count == 1 and first_tweet_text.startswith("Deleted and encrypted backup of"):
        print("Only Deleted and encrypted backup of...")
    else:
        api.update_status(f"Deleted and encrypted backup of {delete_count} Twitter posts from {BEFORE_DAYS} days ago. {GITHUB_ACTIONS_URL}")
