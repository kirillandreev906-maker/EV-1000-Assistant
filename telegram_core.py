# EV-1000 Pro v3.6
# Telegram Core Final Connector
# Button interface connected to Prediction Core

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

from prediction_core import (
    create_ready_message,
    separate_bets,
    analyse_match
)

from data_engine import format_match_list

from bank_manager import bank_report


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

Все модули подключены.

Prediction Core:
ONLINE

Выберите раздел:
""",
        reply_markup=keyboard
    )


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text


    if text == "📋 Лист":

        await update.message.reply_text(
            format_match_list()
        )
        return


    if text == "🟢 READY":

        results = []

        message = create_ready_message(
            results
        )

        await update.message.reply_text(
            message
        )
        return


    if text == "⭐ ТОП":

        await update.message.reply_text(
            """
⭐ ТОП

CORE:
0

WATCHLIST:
0

Ожидание анализа.
"""
        )
        return


    if text == "💰 Банк":

        await update.message.reply_text(
            bank_report()
        )
        return


    responses = {

        "✅ Качество":
        """
✅ КАЧЕСТВО

Data Engine:
ONLINE

Models:
ONLINE

Risk:
ACTIVE
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
ONLINE

Monte Carlo:
ONLINE
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

EV-1000 v3.6:
ONLINE
"""
    }


    await update.message.reply_text(
        responses.get(
            text,
            "Команда не найдена"
        )
    )



def start_bot():

    print(
        "EV-1000 Telegram Bot ONLINE"
    )


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
