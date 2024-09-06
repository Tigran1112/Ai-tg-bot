from fastapi import FastAPI
from bot import bot

app = FastAPI()

@app.get("/")
def read_root():
    return {"status": "running"}

@app.post("/webhook")
def process_webhook(update: dict):
    update = telebot.types.Update.de_json(update)
    bot.process_new_updates([update])
    return {"status": "ok"}