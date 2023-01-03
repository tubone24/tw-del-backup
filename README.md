# tw-del-backup

![img](https://i.imgur.com/BDhkLK8.jpg)

> Save your important tweets while preventing unexpected Twitter burned up.

## これは何？

Twitter API経由で、自分のTweetを定期的に削除します。

一定期間(実行日からxx日)経過しているTweetを抽出して削除します。

削除したTweetは後々から確認したいため、AES256で暗号化された形のJSONで保存されます。 `ex: backup.json.enc`

Tweetにメディアファイル(画像・動画)がある場合、該当の画像・動画を`./media` 配下にAES256で暗号化された形で保存します。複数のビットレートで動画ファイルが作られている場合、一番高ビットレートのものを保存します。

また、削除したくないTweetがある場合は[config.toml](https://github.com/tubone24/tw-del-backup/blob/595cfaf66174e85cda1671b66769f381d4d02196/config.toml)でTweetのIDを指定します。

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
