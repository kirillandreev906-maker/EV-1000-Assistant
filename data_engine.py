from api_connector import get_matches, get_odds

def update_data():
    return {
        "matches": get_matches(),
        "odds": get_odds()
    }
