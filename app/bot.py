import requests
import os
from app.db import SessionLocal
from app.models import User, Alert

BOT_TOKEN = os.getenv("BOT_TOKEN")
BASE_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

def send_message(chat_id, text):
    requests.post(f"{BASE_URL}/sendMessage", json={
        "chat_id": chat_id,
        "text": text
    })

def handle_message(data):
    db = SessionLocal()

    chat_id = str(data["message"]["chat"]["id"])
    text = data["message"].get("text", "")

    # ensure user exists
    if not db.query(User).filter_by(chat_id=chat_id).first():
        db.add(User(chat_id=chat_id))
        db.commit()

    if text == "/start":
        send_message(chat_id, "🎬 Welcome!\n/add movie,city\n/list")

    elif text.startswith("/add"):
        try:
            _, val = text.split(" ", 1)
            movie, city = val.split(",")

            alert = Alert(
                chat_id=chat_id,
                movie=movie.strip(),
                city=city.strip()
            )
            db.add(alert)
            db.commit()

            send_message(chat_id, f"✅ Alert added: {movie} - {city}")

        except:
            send_message(chat_id, "❌ Format: /add movie,city")

    elif text == "/list":
        alerts = db.query(Alert).filter_by(chat_id=chat_id).all()

        if not alerts:
            send_message(chat_id, "No alerts")
        else:
            msg = "\n".join([f"{a.movie} - {a.city}" for a in alerts])
            send_message(chat_id, msg)

    db.close()