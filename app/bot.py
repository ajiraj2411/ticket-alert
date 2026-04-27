import re
import requests
import os
import logging
from app.db import SessionLocal
from app.models import User, Alert

BOT_TOKEN = os.getenv("BOT_TOKEN")
BASE_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"


def send_message(chat_id, text):
    try:
        requests.post(
            f"{BASE_URL}/sendMessage",
            json={"chat_id": chat_id, "text": text},
            timeout=5,
        )
    except Exception as e:
        logging.error("Telegram Error: %s", e)


def validate(movie, city):
    pattern = r"^[a-zA-Z0-9\s\-']+$"
    return (
        movie and city
        and len(movie) < 100
        and len(city) < 50
        and re.match(pattern, movie)
        and re.match(pattern, city)
    )


def handle_message(data):
    db = SessionLocal()

    try:
        chat_id = str(data["message"]["chat"]["id"])
        text = data["message"].get("text", "").strip()

        if not db.query(User).filter_by(chat_id=chat_id).first():
            db.add(User(chat_id=chat_id))
            db.commit()

        if text == "/start":
            send_message(
                chat_id,
                "🎬 Welcome!\n\n/add movie,city\n/list\n/remove movie,city\n/status",
            )

        elif text == "/status":
            active = db.query(Alert).filter_by(chat_id=chat_id, status="active").count()
            triggered = db.query(Alert).filter_by(chat_id=chat_id, status="triggered").count()

            send_message(chat_id, f"📊 Active: {active}\nTriggered: {triggered}")

        elif text.startswith("/add"):
            try:
                movie, city = text.split(" ", 1)[1].split(",", 1)
                movie, city = movie.strip().lower(), city.strip().lower()

                if not validate(movie, city):
                    raise ValueError

                existing = db.query(Alert).filter_by(
                    chat_id=chat_id, movie=movie, city=city, status="active"
                ).first()

                if existing:
                    send_message(chat_id, "⚠️ Already tracking")
                    return

                db.add(Alert(chat_id=chat_id, movie=movie, city=city))
                db.commit()

                send_message(chat_id, f"✅ Added {movie} in {city}")

            except:
                send_message(chat_id, "❌ Format: /add movie,city")

        elif text == "/list":
            alerts = db.query(Alert).filter_by(chat_id=chat_id, status="active").all()

            if not alerts:
                send_message(chat_id, "No alerts")
            else:
                send_message(chat_id, "\n".join([f"{a.movie} - {a.city}" for a in alerts]))

        elif text.startswith("/remove"):
            try:
                movie, city = text.split(" ", 1)[1].split(",", 1)
                movie, city = movie.strip().lower(), city.strip().lower()

                alert = db.query(Alert).filter_by(
                    chat_id=chat_id, movie=movie, city=city, status="active"
                ).first()

                if not alert:
                    send_message(chat_id, "Not found")
                    return

                alert.status = "removed"
                db.commit()

                send_message(chat_id, "Removed")

            except:
                send_message(chat_id, "❌ Format: /remove movie,city")

        else:
            send_message(chat_id, "Unknown command")

    finally:
        db.close()
