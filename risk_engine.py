# EV-1000 Pro v3.6
# Risk Engine Module
# Bank management and stake control

BANK_START = 1000

MAX_DAILY_BETS = 3

MIN_STAKE = 30


def get_bank_status(
    current_bank=BANK_START,
    bets_today=0
):

    return {

        "start_bank":
        BANK_START,

        "current_bank":
        current_bank,

        "bets_today":
        bets_today,

        "remaining_bets":
        max(
            0,
            MAX_DAILY_BETS - bets_today
        ),

        "mode":
        "NORMAL"

    }



def calculate_stake(
    bank,
    confidence,
    edge
):

    """
    Расчёт ставки.
    Используется осторожный режим.
    """

    if confidence < 80:
        return 0


    if edge < 7:
        return 0


    stake = bank * 0.05


    if stake < MIN_STAKE:
        stake = MIN_STAKE


    if stake > 100:
        stake = 100


    return round(
        stake
    )



def risk_check(
    bets_today,
    correlation=False
):

    if bets_today >= MAX_DAILY_BETS:

        return {
            "status":
            "BLOCK",

            "reason":
            "Daily limit reached"
        }


    if correlation:

        return {
            "status":
            "BLOCK",

            "reason":
            "High correlation"
        }


    return {

        "status":
        "OK",

        "reason":
        "Risk acceptable"

    }
