from api_connector import get_matches, get_odds

def update_data():
    return {
        "matches": get_matches(),
        "odds": get_odds()
    }

def format_match_list():
    data=update_data()
    if not data["matches"]:
        return "📋 ЛИСТ МАТЧЕЙ\n\nОжидание API данных"
    return str(data)
