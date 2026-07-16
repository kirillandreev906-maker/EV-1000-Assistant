# EV-1000 Pro v3.6
# Player AI Final Connector
# Lineups, injuries and player impact analysis


def create_player(
    name,
    position,
    rating,
    form,
    status="ACTIVE"
):

    return {
        "name": name,
        "position": position,
        "rating": rating,
        "form": form,
        "status": status
    }



def analyse_lineup(players):

    if not players:

        return {
            "impact": 0,
            "status": "NO DATA"
        }


    total = 0
    active = 0
    unavailable = []


    for player in players:

        if player.get("status") == "ACTIVE":

            total += player.get(
                "rating",
                0
            )

            active += 1

        else:

            unavailable.append(
                player.get("name")
            )


    impact = 0

    if active:

        impact = round(
            total / active,
            2
        )


    return {

        "player_impact": impact,

        "active_players": active,

        "missing_players": unavailable,

        "status": "READY"

    }



def injury_analysis(
    player_rating
):

    if player_rating >= 85:

        return {
            "impact":
            "HIGH",

            "model_adjustment":
            -10
        }


    if player_rating >= 75:

        return {
            "impact":
            "MEDIUM",

            "model_adjustment":
            -5
        }


    return {
        "impact":
        "LOW",

        "model_adjustment":
        -2
    }



def team_squad_report(
    team,
    players
):

    result = analyse_lineup(players)

    return {

        "team":
        team,

        "analysis":
        result

    }
