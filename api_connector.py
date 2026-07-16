# EV-1000 Pro v3.6
# API Data Connector Module
# Preparation for real football data sources


import time


DATA_SOURCES = {

    "matches": "WAITING",

    "odds": "WAITING",

    "lineups": "WAITING",

    "statistics": "WAITING"

}



def connect_source(
    source_name
):

    """
    Подготовка подключения внешних API.

    Будут подключаться:
    - матчи
    - коэффициенты
    - составы
    - статистика
    """

    DATA_SOURCES[source_name] = "CONNECTED"

    return DATA_SOURCES



def get_today_matches():

    """
    Временная структура.
    После подключения API сюда приходят реальные матчи.
    """

    return [

        {
            "match":
            "Example FC - Example United",

            "league":
            "Test League",

            "time_msk":
            "21:00",

            "odds":
            1.80,

            "status":
            "NEW"

        }

    ]



def get_odds(match):

    return {

        "match":
        match,

        "home":
        1.80,

        "draw":
        3.50,

        "away":
        4.20

    }



def update_sources():

    return {

        "status":
        "API CONNECTOR READY",

        "timestamp":
        time.time(),

        "sources":
        DATA_SOURCES

    }
