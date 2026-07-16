# EV-1000 Pro v3.6
# Prediction Core Module

from datetime import datetime


def calculate_prediction(match_data):
    """
    Центральный модуль принятия решения.
    Сейчас работает в SIMULATION режиме.
    """

    return {
        "match": match_data.get("match", "Unknown"),
        "market": "WAITING",
        "probability": 0,
        "edge": 0,
        "risk": "UNKNOWN",
        "status": "ANALYSIS"
    }


def create_ready_report(predictions):

    if not predictions:
        return """
🟢 READY

Подтвержденных ставок нет.

Причина:
нет данных для расчёта.

Mode:
SIMULATION
"""

    report = "🟢 READY\n\nCORE BETS:\n\n"

    for i, item in enumerate(predictions, 1):
        report += f"""
{i}.
Матч: {item.get('match')}
Рынок: {item.get('market')}
Вероятность: {item.get('probability')}%
EV: {item.get('edge')}%
Риск: {item.get('risk')}

"""

    return report


def classify_bets(all_bets):

    """
    Разделение:
    CORE
    WATCHLIST
    """

    sorted_bets = sorted(
        all_bets,
        key=lambda x: x.get("edge", 0),
        reverse=True
    )

    core = sorted_bets[:3]
    watchlist = sorted_bets[3:10]

    return {
        "core": core,
        "watchlist": watchlist,
        "updated": datetime.now()
    }
