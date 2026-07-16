def calculate_ev(probability, odds):
    if not odds:
        return 0
    return round(probability - (100/odds), 2)
