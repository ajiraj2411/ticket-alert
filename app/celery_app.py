from celery import Celery
from datetime import timedelta
import os

celery = Celery(
    "ticket_alert",
    broker=os.getenv("REDIS_URL"),
    backend=os.getenv("REDIS_URL"),
)

CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL", 15))

celery.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)

celery.conf.beat_schedule = {
    "check-alerts": {
        "task": "app.worker.run_worker",
        "schedule": timedelta(seconds=CHECK_INTERVAL),
    },
}
