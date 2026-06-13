import os
from flask import Flask, request
import requests
import random

app = Flask(__name__)
TOKEN = "8883241923:AAHwg34KsO8uhCToiIwJBCiX3bjNhxf3pr8"
MINI_APP = "https://belyash-coder.github.io"

@app.route("/")
def home():
    return "Бот работает!"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"].get("text", "")
        
        if text == "/start":
                        send_message(chat_id, "🎵 Привет! Жми кнопку 👇", [[{"text": "🎰 Открыть рулетку", "web_app": {"url": MINI_APP}}]])
        else:
            send_message(chat_id, "Напиши /start")
    return "ok"

def send_message(chat_id, text, keyboard=None):
    payload = {"chat_id": chat_id, "text": text}
    if keyboard:
        payload["reply_markup"] = {"inline_keyboard": keyboard}
    requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", json=payload)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
