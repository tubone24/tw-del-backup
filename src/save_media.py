import os
from datetime import datetime, timedelta
from encrypt import AESCipher
import requests


def create_file_urls(tweet):
    tweet_id = tweet["id_str"]
    media_urls = []
    if ("extended_entities" in tweet):
        print("extended entities exist")
        if ("media" in tweet["extended_entities"]):
            print("Media exist!")
            for media in tweet["extended_entities"]["media"]:
                file_type = media["type"]
                media_id = media["id_str"]
                if (file_type == "photo"):
                    media_urls.append({"prefix": f"{tweet_id}_{media_id}_{file_type}", "url": media["media_url_https"]})
                elif (file_type == "video"):
                    video_info = media["video_info"]
                    media_urls.append({"prefix": f"{tweet_id}_{media_id}_{file_type}", "url": extract_video_url(video_info)})
                else:
                  print("no MINE/TYPE")
                  print(media)
                    
    return media_urls

def extract_video_url(video_info):
    if ("variants" in video_info):
        max_bitrate = 0
        max_bitrate_url = ""
        for variant in video_info["variants"]:
            if (variant["content_type"] != "application/x-mpegURL" and "bitrate" in variant):
                bitrate = variant["bitrate"]
                if (bitrate >= max_bitrate):
                    max_bitrate = bitrate
                    max_bitrate_url = variant["url"]
        return max_bitrate_url
    else:
        return ""

def save_media(urls, backup_key):
    aes = AESCipher(key=backup_key)
    for media in urls:
        print(media)
        url_data = requests.get(media["url"]).content
        if (len(url_data) <= 0):
            continue
        url_file_name = media["url"].split("/")[-1].replace("?tag=10", "")
        prefix = media["prefix"]
        directory_path = f"media/{prefix}"
        os.makedirs(directory_path, exist_ok=True)
        filename = f"{directory_path}/{url_file_name}"
        with open(filename ,mode='wb') as f:
            f.write(url_data)
        aes.encrypt_bytes(filename, delete_raw_file=True)
        # aes.decrypt_bytes(filename + ".enc", delete_raw_file=True)

def save_tweet_media(tweet, backup_key):
    save_media(create_file_urls(tweet), backup_key)
