# EV-1000 Pro v3.6
# Market AI Module
# Value / Edge calculation engine

def implied_probability(odds):

    if odds <= 0:
        return 0

    return round(
        1 / odds * 100,
        2
    )


def calculate_edge(
    model_probability,
    odds
):

    """
    Сравнение вероятности модели
    с вероятностью рынка.
    """

    market_probability = implied_probability(
        odds
    )


    edge = model_probability - market_probability


    return {

        "model_probability":
        model_probability,

        "market_probability":
        market_probability,

        "edge":
        round(edge, 2),

        "status":
        "VALUE FOUND"
        if edge > 7
        else "NO VALUE"
    }



def analyse_market(
    match,
    market,
    odds,
    model_probability
):

    result = calculate_edge(
        model_probability,
        odds
    )


    return {

        "match":
        match,

        "market":
        market,

        "odds":
        odds,

        "model_probability":
        result["model_probability"],

        "edge":
        result["edge"],

        "status":
        result["status"]

    }
