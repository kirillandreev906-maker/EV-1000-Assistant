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

from prediction_core import create_ready_report, classify_bets

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

Prediction Core:
ONLINE

Выберите раздел:
""",
        reply_markup=keyboard
    )


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text

    if text == "🟢 READY":

        predictions = []

        result = create_ready_report(predictions)

        await update.message.reply_text(result)
        return


    answers = {

        "📋 Лист":
        """
📋 ЛИСТ МАТЧЕЙ

Data Engine:
ACTIVE

Матчи:
ожидание подключения источников
""",

        "⭐ ТОП":
        """
⭐ ТОП

CORE:
0

WATCHLIST:
0

Правило:
3 основные + остальные наблюдение
""",

        "✅ Качество":
        """
✅ КАЧЕСТВО

Data:
CHECK

Model:
READY

Risk:
ACTIVE
""",

        "💰 Банк":
        """
💰 БАНК

Старт:
1000 ₽

Лимит:
3 ставки/сутки

Минимум:
30 ₽
""",

        "📈 Отчет":
        """
📈 ОТЧЕТ

История:
ожидание данных
""",

        "📊 Аналитика":
        """
📊 АНАЛИТИКА

Prediction Core:
ONLINE

Market AI:
READY
""",

        "📖 Журнал":
        """
📖 ЖУРНАЛ

Записей:
0
""",

        "🔄 Обновить":
        """
🔄 ОБНОВЛЕНИЕ

EV-1000 Core:
ONLINE
"""
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
        CommandHandler(
            "start",
            start
        )
    )


    app.add_handler(
        MessageHandler(
            filters.TEXT,
            button_handler
        )
    )


    app.run_polling()
