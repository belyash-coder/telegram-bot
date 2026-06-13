import os
from flask import Flask, request
import requests
import random
import datetime

app = Flask(__name__)
TOKEN = "8883241923:AAHwg34KsO8uhCToiIwJBCiX3bjNhxf3pr8"
MINI_APP = "https://belyash-coder.github.io"

# Загружаем жанры из вашего сайта (из index.html)
GENRES = []
try:
    resp = requests.get("https://belyash-coder.github.io", timeout=10)
    # Извлекаем массив жанров из JS
    start = resp.text.find("const everynoise = `") + 20
    end = resp.text.find("`;", start)
    raw = resp.text[start:end]
    GENRES = [g.strip() for g in raw.split('\n') if g.strip() and len(g.strip()) > 1]
except:
    # Запасной список
    GENRES = ["pop", "rock", "jazz", "blues", "hip hop", "metal", "punk", "folk", "disco", "house"]

@app.route("/")
def home():
    return f"Бот работает! Загружено {len(GENRES)} жанров."

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    
    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"].get("text", "")
        
        if text in ["/start", "/menu", "📋 Меню"]:
            requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", json={
                "chat_id": chat_id,
                "text": "🎵 *Главное меню*\n\nВыбери действие:",
                "parse_mode": "Markdown",
                "reply_markup": {
                    "inline_keyboard": [
                        [{"text": "🎲 Случайный жанр", "callback_data": "genre"}],
                        [{"text": "📅 Жанр дня", "callback_data": "daily"}],
                        [{"text": "🎰 Открыть рулетку", "web_app": {"url": MINI_APP}}],
                        [{"text": "📚 Коллекция", "callback_data": "collection"},
                         {"text": "ℹ️ О боте", "callback_data": "about"}]
                    ]
                }
            })
        
        elif text in ["🎲 Случайный жанр", "/genre"]:
            send_genre(chat_id)
        
        elif text in ["📅 Жанр дня", "/daily"]:
            today = datetime.date.today().toordinal()
            genre = GENRES[today % len(GENRES)]
            requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", json={
                "chat_id": chat_id,
                "text": f"📅 *Жанр дня:* {genre}\n\n[🟢 Spotify](https://open.spotify.com/search/{genre.replace(' ', '%20')})",
                "parse_mode": "Markdown",
                "disable_web_page_preview": True
            })
        
        elif text in ["📚 Коллекция", "/collection"]:
            requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", json={
                "chat_id": chat_id,
                "text": "📚 Коллекция доступна в Mini App!\n\nОткрой приложение и нажми 📚 вверху.",
                "reply_markup": {"inline_keyboard": [[{"text": "🎰 Открыть рулетку", "web_app": {"url": MINI_APP}}]]}
            })
        
        elif text in ["ℹ️ О боте", "/about"]:
            requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", json={
                "chat_id": chat_id,
                "text": "🎵 *Случайный музыкальный жанр*\n\n• Более 5000 жанров\n• Рулетка с анимацией\n• Фильтры по категориям\n• Last.fm + Spotify + EveryNoise",
                "parse_mode": "Markdown"
            })
        
        else:
            send_genre(chat_id)
    
    elif "callback_query" in data:
        chat_id = data["callback_query"]["message"]["chat"]["id"]
        callback_data = data["callback_query"]["data"]
        
        if callback_data == "genre":
            send_genre(chat_id)
        elif callback_data == "daily":
            today = datetime.date.today().toordinal()
            genre = GENRES[today % len(GENRES)]
            requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", json={
                "chat_id": chat_id,
                "text": f"📅 *Жанр дня:* {genre}\n\n[🟢 Spotify](https://open.spotify.com/search/{genre.replace(' ', '%20')})",
                "parse_mode": "Markdown", "disable_web_page_preview": True
            })
        elif callback_data == "collection":
            requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", json={
                "chat_id": chat_id,
                "text": "📚 Коллекция в Mini App!",
                "reply_markup": {"inline_keyboard": [[{"text": "🎰 Открыть", "web_app": {"url": MINI_APP}}]]}
            })
        elif callback_data == "about":
            requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", json={
                "chat_id": chat_id,
                "text": "🎵 *Случайный музыкальный жанр*\n\n• Более 5000 жанров\n• Рулетка с анимацией\n• Фильтры по категориям\n• Last.fm + Spotify + EveryNoise",
                "parse_mode": "Markdown"
            })
        elif callback_data == "menu":
            requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", json={
                "chat_id": chat_id,
                "text": "🎵 *Главное меню*\n\nВыбери действие:",
                "parse_mode": "Markdown",
                "reply_markup": {
                    "inline_keyboard": [
                        [{"text": "🎲 Случайный жанр", "callback_data": "genre"}],
                        [{"text": "📅 Жанр дня", "callback_data": "daily"}],
                        [{"text": "🎰 Открыть рулетку", "web_app": {"url": MINI_APP}}],
                        [{"text": "📚 Коллекция", "callback_data": "collection"},
                         {"text": "ℹ️ О боте", "callback_data": "about"}]
                    ]
                }
            })
        
        requests.post(f"https://api.telegram.org/bot{TOKEN}/answerCallbackQuery", json={
            "callback_query_id": data["callback_query"]["id"]
        })
    
    return "ok"

def send_genre(chat_id):
    genre = random.choice(GENRES)
    slug = ''.join(c for c in genre if c.isalnum()).lower()
    spotify = f"https://open.spotify.com/search/{genre.replace(' ', '%20')}"
    everynoise = f"https://everynoise.com/engenremap-{slug}.html"
    lastfm = f"https://www.last.fm/tag/{genre.replace(' ', '%20')}"
    
    requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", json={
        "chat_id": chat_id,
        "text": f"🎲 *{genre}*\n\n[🔴 Last.fm]({lastfm}) | [🟢 Spotify]({spotify}) | [🔗 EveryNoise]({everynoise})",
        "parse_mode": "Markdown",
        "disable_web_page_preview": True,
        "reply_markup": {
            "inline_keyboard": [
                [{"text": "🔄 Ещё жанр", "callback_data": "genre"},
                 {"text": "📋 Меню", "callback_data": "menu"}]
            ]
        }
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
