import os
from telegram.ext import Application

BOT_TOKEN = os.getenv("BOT_TOKEN")

def start_bot():
    print("EV-1000 Telegram Bot ONLINE")
    if not BOT_TOKEN:
        raise ValueError("BOT_TOKEN missing")
    app = Application.builder().token(BOT_TOKEN).build()
    app.run_polling()
