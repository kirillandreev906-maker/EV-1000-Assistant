from telegram import Update
from telegram.ext import ApplicationBuilder,CommandHandler,ContextTypes
import os
TOKEN=os.getenv("BOT_TOKEN","")
async def start(update:Update,ctx:ContextTypes.DEFAULT_TYPE):
 await update.message.reply_text("EV-1000 Pro Assistant запущен")
async def ready(update:Update,ctx:ContextTypes.DEFAULT_TYPE):
 await update.message.reply_text("READY: подтвержденных ставок нет.")
app=ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start",start))
app.add_handler(CommandHandler("ready",ready))
app.run_polling()
