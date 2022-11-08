import requests
import cv2
import telegram
from telegram import InputMediaPhoto
from bs4 import BeautifulSoup
import json
from PIL import Image
from io import BytesIO

chat_id = 72380774#"@move_to_teriberka"

def lambda_handler(event, context):
    main()

def main():
    bot = telegram.Bot("5427574896:AAExKvRYcHNLrr3x8mO6NDeok1gRL7V3sgU")
    post = "Добрый день\\!\nВ Териберке согодя:\n\n"

    post += get_weather()
    post += get_news()
    post += get_vacancies()
    media_group = get_img()
    
    print(post)
    if len(media_group) > 0:
        media_group[0].parse_mode = telegram.ParseMode.MARKDOWN_V2 
        bot.send_media_group(chat_id=chat_id, media=media_group)
    
    bot.sendMessage(chat_id=chat_id,text = post, parse_mode = telegram.ParseMode.MARKDOWN_V2, disable_web_page_preview = True)
    


def get_weather():
    lat = "69.1641329"
    lon = "35.1458289"
    units = "metric"
    lang = "ru"
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid=e9926914b5d511f8b56f07386ea86d47&units={units}&lang={lang}"
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
        #print(n.string)
        #print(sheld_ch(n.string))
        news += f"[{sheld_ch(n.string)}](https://www.hibiny.com{n['href']})\n"

    return news


def get_img():
    sids = [
        "cc06ae04-3b67-4434-b02a-477cf274ba4c",
        "574a9ba5-58d7-4734-b72f-c304bc617889",
        "c2490a39-1638-4fc1-937e-f2ed3e0d27a9",
    ]
    media_group = []

    for sid in sids:
        try:
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
        except:
            pass

    return media_group

def get_vacancies():
    vacancies = '\n\n*Открытые вакансии:*\n'
    for item in requests.get("https://api.hh.ru/vacancies?area=5402").json()['items']:
        name = sheld_ch(item['name'])
        vacancy = f"[{name}]({item['alternate_url']})"
        if item['salary']['from'] is not None:
            vacancy += f" от {item['salary']['from']} руб\."
        if item['salary']['to'] is not None:
            vacancy += f" до {item['salary']['to']} руб\."
        employee = sheld_ch(item['employer']['name'])
        vacancy += f"\n{sheld_ch(employee)}\n\n"
        vacancies += vacancy
    return vacancies

def sheld_ch(s: str):
    sheld_chars = ['_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!', '–']
    for ch in sheld_chars:
        s = s.replace(ch,'\\' + ch)
    return s
if __name__ == "__main__":
    main()
