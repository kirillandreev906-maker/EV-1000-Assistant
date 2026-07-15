import os

BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()
OWNER_CHAT_ID = os.getenv("OWNER_CHAT_ID", "").strip()
DB_PATH = os.getenv("DB_PATH", "data/ev1000.db")

READY_EDGE_MIN = float(os.getenv("READY_EDGE_MIN", "6"))
READY_QUALITY_MIN = int(os.getenv("READY_QUALITY_MIN", "85"))
READY_RISK_MAX = int(os.getenv("READY_RISK_MAX", "30"))
READY_CHECK_INTERVAL_SECONDS = int(os.getenv("READY_CHECK_INTERVAL_SECONDS", "1800"))
