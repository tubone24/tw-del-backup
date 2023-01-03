# tw-del-backup

![img](https://i.imgur.com/BDhkLK8.jpg)

> Save your important tweets while preventing unexpected Twitter burned up.

## How to use

Decrypt Tweet
```
python src/decrypt_backup.py "YOUR_PASSWORD" backup.json.enc

# 実際見るときはJqでprettyしてね。
cat backup.json | jq -r > backup_pretty.json
```

Decrypt Media
```
python src/decrypt_media.py "YOUR_PASSWORD" media/tweetid_media_id/filename.jpg.enc
```