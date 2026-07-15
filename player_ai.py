# EV-1000 Pro v3.6
# Player AI Module
# Player impact and squad analysis


def analyse_player(
    name,
    rating,
    form,
    status="ACTIVE"
):

    return {

        "player":
        name,

        "rating":
        rating,

        "form":
        form,

        "status":
        status

    }



def calculate_team_player_impact(
    players
):

    if not players:

        return {

            "impact":
            0,

            "status":
            "NO DATA"

        }


    total = 0

    active = 0


    for player in players:

        if player.get("status") == "ACTIVE":

            total += player.get(
                "rating",
                0
            )

            active += 1


    if active == 0:

        return {

            "impact":
            0,

            "status":
            "NO ACTIVE PLAYERS"

        }


    average = total / active


    return {

        "impact":
        round(average,2),

        "players":
        active,

        "status":
        "READY"

    }



def injury_impact(
    rating
):

    """
    Оценка потери игрока.
    """

    if rating >= 85:

        return "HIGH IMPACT"


    if rating >= 75:

        return "MEDIUM IMPACT"


    return "LOW IMPACT"
