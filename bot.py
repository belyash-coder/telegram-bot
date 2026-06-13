import os
from flask import Flask, request
import requests
import random
import datetime

app = Flask(__name__)
TOKEN = "8883241923:AAHwg34KsO8uhCToiIwJBCiX3bjNhxf3pr8"
MINI_APP = "https://belyash-coder.github.io"

GENRES = [
    "pop", "rap", "rock", "hip hop", "reggaeton", "dance pop", "jazz", "blues",
    "metal", "punk", "folk", "country", "electronic", "house", "techno", "trance",
    "dubstep", "ambient", "funk", "soul", "disco", "indie rock", "alternative",
    "shoegaze", "dream pop", "synthwave", "vaporwave", "lo-fi", "drum and bass",
    "deep house", "trap", "classical", "reggae", "r&b", "grunge", "hard rock",
    "heavy metal", "death metal", "black metal", "thrash metal", "doom metal",
    "progressive rock", "psychedelic", "krautrock", "post-punk", "new wave"
]

@app.route("/")
def home():
    return "Бот работает!"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    
    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"].get("text", "")
        
        if text in ["/start", "/menu", "📋 Меню"]:
            send_message(chat_id,
                "🎵 *Главное меню*\n\nВыбери действие:",
                keyboard=[
                    [{"text": "🎲 Случайный жанр"}, {"text": "📅 Жанр дня"}],
                    [{"text": "🎰 Открыть рулетку", "web_app": {"url": MINI_APP}}],
                    [{"text": "📚 Моя коллекция"}, {"text": "ℹ️ О боте"}]
                ]
            )
        elif text in ["🎲 Случайный жанр", "/genre"]:
            genre = random.choice(GENRES)
            slug = ''.join(c for c in genre if c.isalnum()).lower()
            spotify = f"https://open.spotify.com/search/{genre.replace(' ', '%20')}"
            everynoise = f"https://everynoise.com/engenremap-{slug}.html"
            lastfm = f"https://www.last.fm/tag/{genre.replace(' ', '%20')}"
            
            send_message(chat_id,
                f"🎲 *{genre}*\n\n"
                f"[🔴 Last.fm]({lastfm}) | [🟢 Spotify]({spotify}) | [🔗 EveryNoise]({everynoise})"
            )
            # Отправляем клавиатуру отдельным сообщением
            requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", json={
                "chat_id": chat_id,
                "text": "━━━━━━━━━━━━━",
                "reply_markup": {
                    "keyboard": [
                        [{"text": "🎲 Случайный жанр"}, {"text": "📋 Меню"}]
                    ],
                    "resize_keyboard": True,
                    "one_time_keyboard": False
                }
            })
        elif text in ["📅 Жанр дня", "/daily"]:
            today = datetime.date.today().toordinal()
            genre = GENRES[today % len(GENRES)]
            spotify = f"https://open.spotify.com/search/{genre.replace(' ', '%20')}"
            send_message(chat_id, f"📅 *Жанр дня:* {genre}\n\n[🟢 Слушать на Spotify]({spotify})")
        elif text in ["📚 Моя коллекция", "/collection"]:
            send_message(chat_id,
                "📚 Коллекция доступна в Mini App!\n\nОткрой приложение и нажми на 📚 в правом верхнем углу.",
                keyboard=[[{"text": "🎰 Открыть рулетку", "web_app": {"url": MINI_APP}}]]
            )
        elif text in ["ℹ️ О боте", "/about"]:
            send_message(chat_id,
                "🎵 *Случайный музыкальный жанр*\n\n"
                "• Более 5000 жанров\n• Рулетка с анимацией\n"
                "• Фильтры по категориям\n• Коллекция жанров\n"
                "• Last.fm + Spotify + EveryNoise\n\n"
                "Создано для исследования музыки 🎧"
            )
        else:
            genre = random.choice(GENRES)
            slug = ''.join(c for c in genre if c.isalnum()).lower()
            spotify = f"https://open.spotify.com/search/{genre.replace(' ', '%20')}"
            everynoise = f"https://everynoise.com/engenremap-{slug}.html"
            lastfm = f"https://www.last.fm/tag/{genre.replace(' ', '%20')}"
            send_message(chat_id,
                f"🎲 *{genre}*\n\n"
                f"[🔴 Last.fm]({lastfm}) | [🟢 Spotify]({spotify}) | [🔗 EveryNoise]({everynoise})"
            )
    
    return "ok"

def send_message(chat_id, text, keyboard=None):
    payload = {"chat_id": chat_id, "text": text, "disable_web_page_preview": True}
    if "[🔴" in text or "[🟢" in text:
        payload["parse_mode"] = "Markdown"
    if keyboard:
        payload["reply_markup"] = {"inline_keyboard": keyboard}
    requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", json=payload)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
