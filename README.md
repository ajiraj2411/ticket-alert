# BookMyShow Ticket Alert App

A Telegram bot that alerts users when tickets for movies become available on BookMyShow.

## Features

- Telegram bot for managing movie alerts
- Automatic checking for ticket availability
- PostgreSQL database for storing alerts
- Docker support

## Setup

1. Clone the repository
2. Create a `.env` file with the following variables:
   ```
   BOT_TOKEN=your_telegram_bot_token
   DATABASE_URL_PUBLIC=postgresql://user:pass@host:port/db
   REDIS_URL=redis://localhost:6379/0
   CHECK_INTERVAL=15  # seconds between checks
   ```
3. Install dependencies: `pip install -r requirements.txt`
4. Run the app: `uvicorn app.main:app --host 0.0.0.0 --port 8000`
5. Run Celery worker: `celery -A app.celery_app worker --loglevel=info`
6. Run Celery beat for periodic tasks: `celery -A app.celery_app beat --loglevel=info`

## Docker

Build and run with Docker:

```bash
docker build -t ticket-alert .
docker run -p 8000:8000 ticket-alert
```

## Usage

- Start a chat with your bot
- Use `/start` to see commands
- Add alerts with `/add movie,city`
- List alerts with `/list`
- Remove alerts with `/remove movie,city`
- Check status with `/status`

## Testing

Run tests with: `pytest`