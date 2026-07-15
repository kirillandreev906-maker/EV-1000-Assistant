import os

from telegram import Update, ReplyKeyboardMarkup

from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")


MENU = [
    ["📋 Лист", "🟢 READY"],
    ["⭐ ТОП", "✅ Качество"],
    ["💰 Банк", "📈 Отчет"],
    ["📊 Аналитика", "📖 Журнал"],
    ["🔄 Обновить"]
]


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = ReplyKeyboardMarkup(
        MENU,
        resize_keyboard=True
    )

    await update.message.reply_text(
        """
EV-1000 Pro v3.6

Система запущена.

Выберите раздел:
""",
        reply_markup=keyboard
    )


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text

    answers = {
        "📋 Лист": "📋 ЛИСТ МАТЧЕЙ\n\nСканирование: ACTIVE\nData Engine: ожидание",
        "🟢 READY": "🟢 READY\n\nПодтвержденных ставок нет.\nРежим: SIMULATION",
        "⭐ ТОП": "⭐ ТОП\n\nCORE: 0\nWATCHLIST: 0",
        "✅ Качество": "✅ КАЧЕСТВО\n\nData: OK\nModel: READY\nRisk: ACTIVE",
        "💰 Банк": "💰 БАНК\n\nСтарт: 1000 ₽\nЛимит: 3 ставки/сутки",
        "📈 Отчет": "📈 ОТЧЕТ\n\nСтавок: 0\nROI: 0%",
        "📊 Аналитика": "📊 АНАЛИТИКА\n\nPrediction Core: ONLINE\nML: READY",
        "📖 Журнал": "📖 ЖУРНАЛ\n\nИстория пуста",
        "🔄 Обновить": "🔄 ОБНОВЛЕНИЕ\n\nEV-1000 Core CHECK"
    }

    await update.message.reply_text(
        answers.get(text, "Команда не найдена")
    )


def start_bot():

    print("EV-1000 Telegram Bot ONLINE")

    app = Application.builder()\
        .token(BOT_TOKEN)\
        .build()

    app.add_handler(
        CommandHandler("start", start)
    )

    app.add_handler(
        MessageHandler(filters.TEXT, button_handler)
    )

    app.run_polling()
