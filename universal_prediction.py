# EV-1000 Pro v3.6
# Universal Prediction Core
# Main decision fusion engine


from market_ai import calculate_edge
from monte_carlo import simulate_match
from risk_engine import calculate_stake


def combine_models(
    probability,
    edge,
    tactical_score,
    player_impact
):

    score = (

        probability * 0.4 +

        edge * 2 +

        tactical_score * 0.2 +

        player_impact * 0.1

    )

    return round(score, 2)



def make_decision(
    match,
    odds,
    probability,
    confidence,
    edge,
    tactical_score=85,
    player_impact=80,
    bank=1000
):

    quality = combine_models(
        probability,
        edge,
        tactical_score,
        player_impact
    )


    if confidence < 80:

        status = "PASS"


    elif edge < 7:

        status = "WATCHLIST"


    else:

        status = "CORE BET"



    stake = calculate_stake(
        bank,
        confidence,
        edge
    )


    return {

        "match":
        match,

        "odds":
        odds,

        "probability":
        probability,

        "edge":
        edge,

        "quality":
        quality,

        "status":
        status,

        "stake":
        stake

    }



def full_simulation(
    home_strength,
    away_strength
):

    return simulate_match(
        home_strength,
        away_strength,
        10000
    )
