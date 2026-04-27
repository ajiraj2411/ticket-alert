import requests
import os
import logging
from tenacity import retry, stop_after_attempt, wait_exponential
from app.db import SessionLocal
from app.models import Alert
from app.celery_app import celery

BOT_TOKEN = os.getenv("BOT_TOKEN")


def notify(chat_id, msg):
    try:
        requests.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
            json={"chat_id": chat_id, "text": msg},
            timeout=5,
        )
    except Exception as e:
        logging.error("Notify error: %s", e)


@retry(stop=stop_after_attempt(3), wait=wait_exponential(min=4, max=10))
def check_booking(movie, city):
    try:
        res = requests.get(
            f"https://in.bookmyshow.com/api/search?query={movie}", timeout=5
        )
        data = res.json()

        event_id = next((x.get("eventId") for x in data.get("data", []) if "eventId" in x), None)

        if not event_id:
            return False

        res2 = requests.get(
            f"https://in.bookmyshow.com/api/quickbook/{event_id}?city={city}",
            timeout=5,
        )

        show_data = res2.json()

        return bool(show_data.get("venues") or show_data.get("showtimes"))

    except Exception as e:
        logging.error("Check error: %s", e)

    return False


@celery.task(name="app.worker.run_worker")
def run_worker():
    db = SessionLocal()

    alerts = db.query(Alert).filter_by(status="active").all()

    # 🔥 GROUPING (OPTIMIZATION)
    grouped = {}
    for alert in alerts:
        key = (alert.movie, alert.city)
        grouped.setdefault(key, []).append(alert)

    for (movie, city), group_alerts in grouped.items():
        logging.info("Checking %s in %s", movie, city)

        if check_booking(movie, city):
            for alert in group_alerts:
                notify(alert.chat_id, f"🎟️ {movie} OPEN in {city}")
                alert.status = "triggered"

            db.commit()

    db.close()
