import requests
import cv2
import telegram
from telegram import InputMediaPhoto
from bs4 import BeautifulSoup
import json

SETTINGS = json.load(open("settings.json", "r"))


def main():
    bot = telegram.Bot(SETTINGS["bot_token"])
    post = "Добрый день\\!\nВ Териберке согодя:\n\n"

    post += get_weather()
    post += get_news()

    get_img()

    media_group = []
    media_group.append(
        InputMediaPhoto(open(f"cc06a.jpeg", "rb"), caption=post, parse_mode=telegram.ParseMode.MARKDOWN_V2)
    )
    media_group.append(InputMediaPhoto(open(f"574a9.jpeg", "rb")))
    media_group.append(InputMediaPhoto(open(f"c2490.jpeg", "rb")))

    bot.send_media_group(chat_id=SETTINGS["chat_id"], media=media_group)


def get_weather():
    lat = "69.1641329"
    lon = "35.1458289"
    units = "metric"
    lang = "ru"
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={SETTINGS['weather_api_key']}&units={units}&lang={lang}"
    j = requests.get(url).json()
    temp = round(j["main"]["temp"])
    feels_like = round(j["main"]["feels_like"])
    description = j["weather"][0]["description"].capitalize()
    return f"*ПОГОДА:*\n{description}\nТемпература {temp}°\nОщущается как {feels_like}°"


def get_news():
    response = requests.get(f"https://www.hibiny.com/news/teriberka/")

    soup = BeautifulSoup(requests.get(f"https://www.hibiny.com/news/teriberka/").text, "html.parser")
    news = "\n\n*НОВОСТИ:*\n"
    for n in soup.findAll("a", {"class": "p", "style": "font-size:19px;"})[:5]:
        news += f"[{n.string}](https://www.hibiny.com{n['href']})\n"

    return news.replace(".", "\.")


def get_img():
    sids = [
        "cc06ae04-3b67-4434-b02a-477cf274ba4c",
        "574a9ba5-58d7-4734-b72f-c304bc617889",
        "c2490a39-1638-4fc1-937e-f2ed3e0d27a9",
    ]

    for sid in sids:
        sub_url = requests.get(f"https://streamer.camera.rt.ru/public/master.m3u8?sid={sid}").text.split()[6]
        url = f"https://streamer.camera.rt.ru{sub_url}"
        video = cv2.VideoCapture(url)
        cv2.imwrite(f"{sid[:5]}.jpeg", video.read()[1])


if __name__ == "__main__":
    main()
