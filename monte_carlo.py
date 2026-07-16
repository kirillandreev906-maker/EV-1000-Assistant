# EV-1000 Pro v3.6
# Monte Carlo Simulation Engine
# Score and probability simulation


import random


def simulate_match(
    home_strength,
    away_strength,
    iterations=10000
):

    home_wins = 0
    draws = 0
    away_wins = 0


    for _ in range(iterations):

        home_goals = max(
            0,
            int(
                random.gauss(
                    home_strength,
                    1
                )
            )
        )


        away_goals = max(
            0,
            int(
                random.gauss(
                    away_strength,
                    1
                )
            )
        )


        if home_goals > away_goals:

            home_wins += 1

        elif home_goals == away_goals:

            draws += 1

        else:

            away_wins += 1



    return {

        "home_win":
        round(home_wins / iterations * 100, 2),

        "draw":
        round(draws / iterations * 100, 2),

        "away_win":
        round(away_wins / iterations * 100, 2),

        "iterations":
        iterations

    }



def top_scores():

    return [

        {
            "score":
            "1:0",

            "probability":
            18
        },

        {
            "score":
            "1:1",

            "probability":
            14
        },

        {
            "score":
            "2:0",

            "probability":
            12
        }

    ]
