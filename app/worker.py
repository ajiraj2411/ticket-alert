import os
import time
import requests
from celery import Celery
from app.db import SessionLocal
from app.models import Alert

REDIS_URL = os.getenv("REDIS_URL")

celery = Celery("worker", broker=REDIS_URL, backend=REDIS_URL)

BOT_TOKEN = os.getenv("BOT_TOKEN")

def notify(chat_id, msg):
    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        json={"chat_id": chat_id, "text": msg}
    )

def fake_check(movie, city):
    # 🔥 replace with real API detection later
    return False


@celery.task
def run_worker():
    db = SessionLocal()

    alerts = db.query(Alert).filter_by(status="active").all()

    for alert in alerts:
        if fake_check(alert.movie, alert.city):
            notify(alert.chat_id, f"🎟️ {alert.movie} OPEN in {alert.city}")

            alert.status = "triggered"
            db.commit()

    db.close()


# loop runner
if __name__ == "__main__":
    while True:
        run_worker.delay()
        time.sleep(20)