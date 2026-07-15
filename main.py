import json
import logging
import os
import sqlite3
from datetime import datetime
from zoneinfo import ZoneInfo

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    ApplicationBuilder,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
)

logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    level=logging.INFO,
)

BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()
OWNER_CHAT_ID = os.getenv("OWNER_CHAT_ID", "").strip()
DB_PATH = os.getenv("DB_PATH", "ev1000.db")
MOSCOW = ZoneInfo("Europe/Moscow")

READY_EDGE_MIN = float(os.getenv("READY_EDGE_MIN", "6"))
READY_QUALITY_MIN = int(os.getenv("READY_QUALITY_MIN", "85"))
READY_RISK_MAX = int(os.getenv("READY_RISK_MAX", "30"))

def connect():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with connect() as conn:
        conn.executescript("""
        CREATE TABLE IF NOT EXISTS matches (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            time_msk TEXT NOT NULL,
            league TEXT NOT NULL,
            home TEXT NOT NULL,
            away TEXT NOT NULL,
            bet TEXT DEFAULT '',
            odds REAL DEFAULT 0,
            probability REAL DEFAULT 0,
            quality INTEGER DEFAULT 0,
            risk INTEGER DEFAULT 100,
            status TEXT DEFAULT 'WAIT',
            note TEXT DEFAULT ''
        );

        CREATE TABLE IF NOT EXISTS bank (
            id INTEGER PRIMARY KEY CHECK(id = 1),
            start REAL NOT NULL,
            current REAL NOT NULL
        );

        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            match_name TEXT NOT NULL,
            bet TEXT NOT NULL,
            odds REAL NOT NULL,
            stake REAL NOT NULL,
            result TEXT NOT NULL,
            profit REAL NOT NULL,
            created_at TEXT NOT NULL
        );

        INSERT OR IGNORE INTO bank(id, start, current) VALUES(1, 1000, 967);
        """)

def is_owner(update: Update) -> bool:
    if not OWNER_CHAT_ID:
        return False
    return str(update.effective_chat.id) == OWNER_CHAT_ID

def calc_edge(probability: float, odds: float) -> float:
    if odds <= 1:
        return 0.0
    return round(probability - (100 / odds), 2)

def calc_ev(probability: float, odds: float) -> float:
    if probability <= 0 or odds <= 1:
        return 0.0
    return round(((probability / 100) * odds - 1) * 100, 2)

def calc_status(probability: float, odds: float, quality: int, risk: int) -> str:
    edge = calc_edge(probability, odds)
    if probability <= 0 or odds <= 1 or quality < 60:
        return "SKIP"
    if quality >= READY_QUALITY_MIN and edge >= READY_EDGE_MIN and risk <= READY_RISK_MAX:
        return "READY"
    return "WAIT"

def main_menu(owner: bool = False) -> InlineKeyboardMarkup:
    rows = [
        [
            InlineKeyboardButton("📋 Лист", callback_data="list"),
            InlineKeyboardButton("🟢 READY", callback_data="ready"),
        ],
        [
            InlineKeyboardButton("⭐ ТОП", callback_data="top"),
            InlineKeyboardButton("✅ Качество", callback_data="quality"),
        ],
        [
            InlineKeyboardButton("💰 Банк", callback_data="bank"),
            InlineKeyboardButton("📈 Отчет", callback_data="report"),
        ],
        [
            InlineKeyboardButton("📊 Аналитика", callback_data="analytics"),
            InlineKeyboardButton("📖 Журнал", callback_data="history"),
        ],
        [InlineKeyboardButton("🔄 Обновить", callback_data="menu")],
    ]
    if owner:
        rows.append([InlineKeyboardButton("⚙️ Панель владельца", callback_data="admin")])
    return InlineKeyboardMarkup(rows)

def admin_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("➕ Добавить тестовый матч", callback_data="admin_add_demo")],
        [InlineKeyboardButton("💰 Банк = 967 ₽", callback_data="admin_bank_967")],
        [InlineKeyboardButton("🧹 Очистить тестовые матчи", callback_data="admin_clear")],
        [InlineKeyboardButton("⬅️ Главное меню", callback_data="menu")],
    ])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.effective_message.reply_text(
        "🤖 EV-1000 Pro v1.0\n\nУправление через кнопки.",
        reply_markup=main_menu(is_owner(update)),
    )

def fetch_matches():
    with connect() as conn:
        rows = conn.execute("SELECT * FROM matches ORDER BY date, time_msk").fetchall()
    result = []
    for row in rows:
        m = dict(row)
        m["edge"] = calc_edge(m["probability"], m["odds"])
        m["ev"] = calc_ev(m["probability"], m["odds"])
        m["status"] = calc_status(m["probability"], m["odds"], m["quality"], m["risk"])
        result.append(m)
    return result

def bank_summary():
    with connect() as conn:
        bank = dict(conn.execute("SELECT * FROM bank WHERE id=1").fetchone())
        rows = conn.execute("SELECT * FROM history").fetchall()
    history = [dict(r) for r in rows]
    wins = sum(1 for r in history if r["result"] == "WIN")
    losses = sum(1 for r in history if r["result"] == "LOSS")
    staked = sum(float(r["stake"]) for r in history)
    profit = float(bank["current"]) - float(bank["start"])
    roi = round((profit / staked * 100), 2) if staked else 0
    winrate = round((wins / (wins + losses) * 100), 2) if wins + losses else 0
    return {**bank, "profit": profit, "roi": roi, "winrate": winrate, "bets": len(history)}

async def callback_router(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    action = q.data

    if action == "menu":
        await q.edit_message_text(
            "🤖 EV-1000 Pro v1.0\n\nВыбери раздел.",
            reply_markup=main_menu(is_owner(update)),
        )
        return

    if action == "list":
        matches = fetch_matches()
        if not matches:
            text = "📋 Лист пуст."
        else:
            lines = ["📋 Лист на 24 часа", ""]
            for m in matches:
                icon = {"READY":"🟢","WAIT":"🟡","SKIP":"🔴"}.get(m["status"], "⚪")
                lines += [
                    f"{icon} #{m['id']} · {m['time_msk']} МСК",
                    f"🏆 {m['league']}",
                    f"⚽ {m['home']} — {m['away']}",
                    f"Статус: {m['status']}",
                    "",
                ]
            text = "\n".join(lines)
        await q.edit_message_text(text, reply_markup=main_menu(is_owner(update)))
        return

    if action == "ready":
        matches = [m for m in fetch_matches() if m["status"] == "READY"]
        if not matches:
            text = "🔴 READY\n\nПодтвержденных ставок нет."
        else:
            lines = ["🟢 READY", ""]
            for m in matches:
                lines += [
                    f"🕒 {m['time_msk']} МСК",
                    f"🏆 {m['league']}",
                    f"⚽ {m['home']} — {m['away']}",
                    f"🎯 {m['bet'] or '—'}",
                    f"📈 КФ {m['odds']}",
                    f"⭐ Edge {m['edge']}%",
                    f"🧮 EV {m['ev']}%",
                    "",
                ]
            text = "\n".join(lines)
        await q.edit_message_text(text, reply_markup=main_menu(is_owner(update)))
        return

    if action == "bank":
        b = bank_summary()
        text = (
            "💰 Банк\n\n"
            f"Старт: {b['start']} ₽\n"
            f"Текущий: {b['current']} ₽\n"
            f"Результат: {b['profit']} ₽\n"
            f"ROI: {b['roi']}%\n"
            f"WinRate: {b['winrate']}%\n"
            f"Ставок: {b['bets']}"
        )
        await q.edit_message_text(text, reply_markup=main_menu(is_owner(update)))
        return

    if action in {"analytics", "top", "quality"}:
        matches = fetch_matches()
        if action == "top":
            matches = sorted(matches, key=lambda m: (m["edge"], m["quality"], -m["risk"]), reverse=True)[:3]
            title = "⭐ ТОП-3"
        elif action == "quality":
            matches = sorted(matches, key=lambda m: m["quality"], reverse=True)
            title = "✅ Качество"
        else:
            title = "📊 Аналитика"

        lines = [title, ""]
        for m in matches:
            lines += [
                f"#{m['id']} {m['home']} — {m['away']}",
                f"🏆 {m['league']} | 🕒 {m['time_msk']} МСК",
                f"Статус: {m['status']}",
                f"КФ: {m['odds']} | Вероятность: {m['probability']}%",
                f"Edge: {m['edge']}% | EV: {m['ev']}%",
                f"Quality: {m['quality']}/100 | Risk: {m['risk']}/100",
                "",
            ]
        if not matches:
            lines.append("Нет данных.")
        await q.edit_message_text("\n".join(lines), reply_markup=main_menu(is_owner(update)))
        return

    if action == "history":
        with connect() as conn:
            rows = conn.execute("SELECT * FROM history ORDER BY id DESC LIMIT 20").fetchall()
        lines = ["📖 Журнал", ""]
        for r in rows:
            d = dict(r)
            lines += [
                f"{d['match_name']}",
                f"{d['bet']} @ {d['odds']} · {d['stake']} ₽",
                f"{d['result']} · {d['profit']} ₽",
                "",
            ]
        if not rows:
            lines.append("Журнал пуст.")
        await q.edit_message_text("\n".join(lines), reply_markup=main_menu(is_owner(update)))
        return

    if action == "report":
        matches = fetch_matches()
        b = bank_summary()
        text = (
            "📈 Отчет\n\n"
            f"Матчей: {len(matches)}\n"
            f"READY: {sum(m['status']=='READY' for m in matches)}\n"
            f"WAIT: {sum(m['status']=='WAIT' for m in matches)}\n"
            f"SKIP: {sum(m['status']=='SKIP' for m in matches)}\n\n"
            f"Банк: {b['current']} ₽\n"
            f"Результат: {b['profit']} ₽\n"
            f"Обновлено: {datetime.now(MOSCOW).strftime('%d.%m.%Y %H:%M МСК')}"
        )
        await q.edit_message_text(text, reply_markup=main_menu(is_owner(update)))
        return

    if action == "admin":
        if not is_owner(update):
            await q.answer("Нет доступа", show_alert=True)
            return
        await q.edit_message_text("⚙️ Панель владельца", reply_markup=admin_menu())
        return

    if action == "admin_add_demo":
        if not is_owner(update):
            return
        with connect() as conn:
            conn.execute(
                """
                INSERT INTO matches(date,time_msk,league,home,away,bet,odds,probability,quality,risk,note)
                VALUES(?,?,?,?,?,?,?,?,?,?,?)
                """,
                (
                    datetime.now(MOSCOW).strftime("%Y-%m-%d"),
                    "20:00",
                    "Тестовый турнир",
                    "Команда А",
                    "Команда Б",
                    "ТМ 2.5",
                    1.90,
                    60,
                    90,
                    25,
                    "Тестовая карточка для проверки интерфейса.",
                ),
            )
        await q.edit_message_text("✅ Тестовый матч добавлен.", reply_markup=admin_menu())
        return

    if action == "admin_bank_967":
        if not is_owner(update):
            return
        with connect() as conn:
            conn.execute("UPDATE bank SET current=967 WHERE id=1")
        await q.edit_message_text("✅ Банк установлен: 967 ₽", reply_markup=admin_menu())
        return

    if action == "admin_clear":
        if not is_owner(update):
            return
        with connect() as conn:
            conn.execute("DELETE FROM matches WHERE league='Тестовый турнир'")
        await q.edit_message_text("✅ Тестовые матчи удалены.", reply_markup=admin_menu())
        return

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    logging.exception("Ошибка бота", exc_info=context.error)

def main():
    if not BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN не задан в Railway Variables.")

    init_db()
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("menu", start))
    app.add_handler(CallbackQueryHandler(callback_router))
    app.add_error_handler(error_handler)
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
