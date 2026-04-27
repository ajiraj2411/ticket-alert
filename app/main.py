from fastapi import FastAPI, Request
from app.db import Base, engine
from app.bot import handle_message

app = FastAPI()

# create tables
Base.metadata.create_all(bind=engine)

@app.post("/webhook")
async def webhook(req: Request):
    data = await req.json()

    if "message" in data:
        handle_message(data)

    return {"ok": True}