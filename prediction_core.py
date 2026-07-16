# EV-1000 Pro v3.6
# Final Prediction Core Connector
# Connects all analysis modules


from universal_prediction import make_decision


def analyse_match(match_data):

    result = make_decision(

        match=match_data.get(
            "match",
            "Unknown"
        ),

        odds=match_data.get(
            "odds",
            0
        ),

        probability=match_data.get(
            "probability",
            0
        ),

        confidence=match_data.get(
            "confidence",
            0
        ),

        edge=match_data.get(
            "edge",
            0
        ),

        tactical_score=match_data.get(
            "tactical_score",
            85
        ),

        player_impact=match_data.get(
            "player_impact",
            80
        ),

        bank=match_data.get(
            "bank",
            1000
        )

    )

    return result



def create_ready_message(results):

    if not results:

        return """
🟢 READY

Подтвержденных ставок нет.

EV-1000 продолжает анализ.
"""


    text = """
🟢 EV-1000 READY

"""

    for i, item in enumerate(results, 1):

        text += f"""
{i}.
Матч:
{item['match']}

Статус:
{item['status']}

Вероятность:
{item['probability']}%

EV:
{item['edge']}%

Ставка:
{item['stake']} ₽

"""

    return text



def separate_bets(results):

    core = []
    watchlist = []


    for item in results:

        if item.get("status") == "CORE BET":

            core.append(item)

        elif item.get("status") == "WATCHLIST":

            watchlist.append(item)


    return {

        "core":
        core,

        "watchlist":
        watchlist

    }
