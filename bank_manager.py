# EV-1000 Pro v3.6
# Bank Manager Module
# Bank tracking, ROI and betting history

START_BANK = 1000


BANK_DATA = {
    "start": START_BANK,
    "current": START_BANK,
    "profit": 0,
    "bets": 0,
    "wins": 0,
    "losses": 0
}


def get_bank():

    return BANK_DATA



def add_bet(
    stake
):

    BANK_DATA["bets"] += 1

    return BANK_DATA



def update_result(
    stake,
    result
):

    if result == "WIN":

        BANK_DATA["current"] += stake
        BANK_DATA["profit"] += stake
        BANK_DATA["wins"] += 1


    elif result == "LOSS":

        BANK_DATA["current"] -= stake
        BANK_DATA["profit"] -= stake
        BANK_DATA["losses"] += 1


    return BANK_DATA



def calculate_roi():

    if BANK_DATA["start"] == 0:
        return 0


    return round(
        BANK_DATA["profit"] /
        BANK_DATA["start"] *
        100,
        2
    )



def bank_report():

    return f"""
💰 БАНК EV-1000


Старт:
{BANK_DATA['start']} ₽


Текущий:
{BANK_DATA['current']} ₽


Прибыль:
{BANK_DATA['profit']} ₽


Ставок:
{BANK_DATA['bets']}


Побед:
{BANK_DATA['wins']}


Поражений:
{BANK_DATA['losses']}


ROI:
{calculate_roi()}%
"""
