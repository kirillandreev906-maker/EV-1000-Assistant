# Existing Telegram bot integration
# Uses buttons instead of slash commands

def start_bot():
    print('EV-1000 Existing Telegram Bot Updated')


BUTTONS = [
    '📋 Лист матчей',
    '🔥 READY',
    '📊 Аналитика',
    '💰 Банк',
    '📈 Отчёты',
    '🤖 Модель',
    '⚡ Live',
    '⚙️ Система'
]


def handle_button(name):
    responses = {
        '🔥 READY':'CORE: нет подтвержденных ставок',
        '💰 Банк':'Банк: 1000 ₽ | Риск: NORMAL',
        '⚙️ Система':'EV-1000 v3.6 ONLINE'
    }
    return responses.get(name, 'EV-1000 обработал запрос')
