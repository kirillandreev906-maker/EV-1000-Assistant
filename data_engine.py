# EV-1000 Pro v3.6
# Data Engine Module
# Simulation + API ready architecture

from datetime import datetime, timezone, timedelta


MATCH_DATABASE = []


def get_moscow_time():

    moscow = timezone(
        timedelta(hours=3)
    )

    return datetime.now(
        moscow
    )


def add_match(
    home,
    away,
    league,
    kickoff
):

    match = {

        "home": home,

        "away": away,

        "league": league,

        "kickoff": kickoff,

        "status": "WAITING",

        "analysis": False
    }


    MATCH_DATABASE.append(match)

    return match



def get_matches():

    """
    Возвращает список матчей
    для кнопки 📋 Лист
    """

    if not MATCH_DATABASE:

        return [

            {
            "home": "Example FC",
            "away": "Example United",
            "league": "Test League",
            "kickoff": "21:00 МСК",
            "status": "WAITING"
            }

        ]


    return MATCH_DATABASE



def format_match_list():

    matches = get_matches()


    text = "📋 ЛИСТ МАТЧЕЙ\n\n"


    for i, match in enumerate(matches,1):

        text += f"""
{i}.
{match['home']} - {match['away']}

Лига:
{match['league']}

Время:
{match['kickoff']}

Статус:
{match['status']}

"""


    return text



def update_data():

    """
    Точка подключения API.
    В дальнейшем сюда подключаются:
    - футбольные API
    - коэффициенты
    - составы
    - статистика
    """


    return {

        "status": "DATA ENGINE ONLINE",

        "updated":
        get_moscow_time().strftime(
            "%d.%m.%Y %H:%M"
        ),

        "matches":
        len(MATCH_DATABASE)

    }
