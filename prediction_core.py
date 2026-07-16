def analyse(match):
    return {
        "match": match,
        "status":"ANALYSIS"
    }

def create_ready_message(results):
    if not results:
        return "🟢 READY\n\nНет подтвержденных ставок."
    return str(results)
