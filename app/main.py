from fastapi import FastAPI, Request
import os, requests

app = FastAPI()

BOT_TOKEN = os.getenv("BOT_TOKEN")

def send_message(chat_id, text):
    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        json={"chat_id": chat_id, "text": text}
    )

@app.post("/webhook")
async def webhook(req: Request):
    data = await req.json()

    if "message" not in data:
        return {"ok": True}

    chat_id = data["message"]["chat"]["id"]
    text = data["message"].get("text", "")

    if text == "/start":
        send_message(chat_id, "🎬 Welcome!\nUse:\n/add movie,city\n/list")

    elif text.startswith("/add"):
        send_message(chat_id, "✅ Alert saved (demo)")

    elif text == "/list":
        send_message(chat_id, "📌 No alerts yet")

    return {"ok": True}