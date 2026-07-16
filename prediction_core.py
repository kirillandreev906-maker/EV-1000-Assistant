def create_ready_message(results):
    if not results:
        return "🟢 READY\n\nПодтвержденных ставок нет."
    return str(results)
