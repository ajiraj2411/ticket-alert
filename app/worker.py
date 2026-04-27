from celery import Celery
import os, requests

celery = Celery(
    "worker",
    broker=os.getenv("REDIS_URL"),
    backend=os.getenv("REDIS_URL")
)

BOT_TOKEN = os.getenv("BOT_TOKEN")

def notify(chat_id, msg):
    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        json={"chat_id": chat_id, "text": msg}
    )

@celery.task
def test_alert():
    notify("YOUR_CHAT_ID", "🚀 Worker is working!")