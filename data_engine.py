# EV-1000 Pro v3.6
# Data Engine Final Connector
# Connects API Connector with EV-1000 Core

from datetime import datetime, timezone, timedelta

from api_connector import (
    get_today_matches,
    get_odds,
    update_sources
)


MATCH_CACHE = []


def moscow_time():

    tz = timezone(
        timedelta(hours=3)
    )

    return datetime.now(tz)



def update_data():

    """
    Обновление данных из API Connector
    """

    global MATCH_CACHE

    matches = get_today_matches()

    MATCH_CACHE = matches


    return {

        "status":
        "DATA ENGINE ONLINE",

        "matches":
        len(matches),

        "updated":
        moscow_time().strftime(
            "%d.%m.%Y %H:%M"
        ),

        "sources":
        update_sources()

    }



def get_matches():

    if not MATCH_CACHE:

        update_data()

    return MATCH_CACHE



def format_match_list():

    matches = get_matches()


    text = "📋 ЛИСТ МАТЧЕЙ\n\n"


    for i, match in enumerate(matches, 1):

        text += f"""
{i}. {match['match']}

Лига:
{match['league']}

Время МСК:
{match['time_msk']}

Коэффициенты:
{get_odds(match['match'])}

Статус:
{match['status']}

"""


    return text
