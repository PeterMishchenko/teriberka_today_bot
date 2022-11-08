import requests
import cv2
import telegram
from telegram import InputMediaPhoto
from bs4 import BeautifulSoup
import json
from PIL import Image
from io import BytesIO

SETTINGS = json.load(open("settings.json", "r"))


bot = telegram.Bot(SETTINGS["bot_token"])
media_group = []
sid = "c2490a39-1638-4fc1-937e-f2ed3e0d27a9"
sub_url = requests.get(f"https://streamer.camera.rt.ru/public/master.m3u8?sid={sid}").text.split()[6]
url = f"https://streamer.camera.rt.ru{sub_url}"
video = cv2.VideoCapture(url)
a,b = video.read()
img = Image.fromarray(cv2.cvtColor(b, cv2.COLOR_BGR2RGB))
bio = BytesIO()
bio.name = 'image.jpeg'
img.save(bio, 'JPEG')
bio.seek(0)
media_group.append(InputMediaPhoto(bio))


bot.send_media_group(chat_id=SETTINGS["chat_id"], media=media_group)
#bot.sendMessage(chat_id=SETTINGS["chat_id"],text = 'yesadjhfkajdsfkjan', parse_mode = telegram.ParseMode.MARKDOWN_V2)