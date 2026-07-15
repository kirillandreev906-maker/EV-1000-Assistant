import logging
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler

from config import BOT_TOKEN
from handlers.start import start
from handlers.help import help_command
from handlers.list_handler import list_command
from handlers.ready import ready
from handlers.bank import bank
from handlers.analytics import analytics
from handlers.match import match_command
from handlers.report import report
from handlers.history import history
from handlers.menu import menu
from handlers.callbacks import button_router
from handlers.admin_wizard import build_admin_conversation
from handlers.match_callback import match_callback
from handlers.top import top
from handlers.quality import quality
from handlers.admin import (
    add_match,
    update_match,
    delete_match,
    settle_bet,
    set_bank,
)
from services.database import init_db
from services.notifier import register_ready_notifier

logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    level=logging.INFO,
)

def build_application():
    if not BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN не задан.")

    init_db()

    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("list", list_command))
    app.add_handler(CommandHandler("ready", ready))
    app.add_handler(CommandHandler("bank", bank))
    app.add_handler(CommandHandler("analytics", analytics))
    app.add_handler(CommandHandler("match", match_command))
    app.add_handler(CommandHandler("report", report))
    app.add_handler(CommandHandler("history", history))
    app.add_handler(CommandHandler("menu", menu))
    app.add_handler(CommandHandler("top", top))
    app.add_handler(CommandHandler("quality", quality))

    app.add_handler(CommandHandler("addmatch", add_match))
    app.add_handler(CommandHandler("updatematch", update_match))
    app.add_handler(CommandHandler("deletematch", delete_match))
    app.add_handler(CommandHandler("settle", settle_bet))
    app.add_handler(CommandHandler("setbank", set_bank))


    app.add_handler(build_admin_conversation())
    app.add_handler(CallbackQueryHandler(match_callback, pattern=r"^match:\\d+$"))
    app.add_handler(CallbackQueryHandler(button_router))

    register_ready_notifier(app)
    return app

if __name__ == "__main__":
    build_application().run_polling(drop_pending_updates=True)