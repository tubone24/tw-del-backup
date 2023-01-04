# tw-del-backup

![img](https://i.imgur.com/BDhkLK8.jpg)

> Save your important tweets while preventing unexpected Twitter burned up.

## これは何？

過去にふとつぶやいたつぶやきが突然炎上するケースがあるので、Twitter API経由で、自分のTweetを定期的に削除します。 [参考](https://japan.cnet.com/article/35120677/)

一定期間(実行日からxx日)経過しているTweetを抽出して削除します。

削除したTweetは後々から確認したいため、AES256で暗号化された形のJSONで保存されます。 `ファイル名: backup.json.enc`

また、暗号化されたJSONファイルは巨大になると、暗号化・復号に時間がかかるため、定期的にローテートします。 [archive](https://github.com/tubone24/tw-del-backup/tree/main/archive) 内にローテートの上移動されます。

Tweetにメディアファイル(画像・動画)がある場合、該当の画像・動画を`./media` 配下にAES256で暗号化された形で保存します。複数のビットレートで動画ファイルが作られている場合、一番高ビットレートのものを保存します。

また、削除したくないTweetがある場合は[config.toml](https://github.com/tubone24/tw-del-backup/blob/595cfaf66174e85cda1671b66769f381d4d02196/config.toml)でTweetのIDを指定します。

### やれていないこと

改ざん防止のためのダイジェスト発行・検証の機能がないです。 GitHubを全面的に信頼している作りなので、git reflogなど使えばファイルの変更は追いきれるとは思っており、改ざんについて想定されませんが、

万が一中身を変えられてしまったときに検知の施しようがないので、この点がネックかもしれません。

## How to use

Decrypt Tweet JSON
```
python src/decrypt_backup.py "YOUR_PASSWORD" backup.json.enc

# 実際見るときはJqでprettyしてね。
cat backup.json | jq -r > backup_pretty.json
```

Decrypt All Tweet JSON (dir)

```
python src/decrypt_all_backup.py "YOUR_PASSWORD" archives/2021
```

Decrypt Media
```
python src/decrypt_media.py "YOUR_PASSWORD" media/tweetid_media_id/filename.jpg.enc
```
