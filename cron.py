import requests
import datetime

TOKEN = "8883241923:AAHwg34KsO8uhCToiIwJBCiX3bjNhxf3pr8"
MINI_APP = "https://belyash-coder.github.io"

# Список жанров
GENRES = []
try:
    resp = requests.get("https://belyash-coder.github.io", timeout=10)
    start = resp.text.find("const everynoise = `") + 20
    end = resp.text.find("`;", start)
    raw = resp.text[start:end]
    GENRES = [g.strip() for g in raw.split('\n') if g.strip() and len(g.strip()) > 1]
except:
    GENRES = ["pop", "rock", "jazz", "blues", "hip hop", "metal", "punk", "folk"]

# ID пользователей, которые подписались на рассылку
subscribers = set()

def send_daily():
    today = datetime.date.today().toordinal()
    genre = GENRES[today % len(GENRES)]
    spotify = f"https://open.spotify.com/search/{genre.replace(' ', '%20')}"
    everynoise = f"https://everynoise.com/engenremap-{''.join(c for c in genre if c.isalnum()).lower()}.html"
    
    text = f"📅 *Жанр дня:* {genre}\n\n[🟢 Spotify]({spotify}) | [🔗 EveryNoise]({everynoise})\n\n🎰 [Открыть рулетку]({MINI_APP})"
    
    for user_id in subscribers:
        try:
            requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", json={
                "chat_id": user_id,
                "text": text,
                "parse_mode": "Markdown",
                "disable_web_page_preview": True
            })
        except:
            pass

if __name__ == "__main__":
    send_daily()
