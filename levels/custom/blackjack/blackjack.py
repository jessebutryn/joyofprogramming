from pyjop import *

SimEnv.connect() and SimEnvManager.first().reset(stop_code=False)
hit = PushButton.find("hit")
stand = PushButton.find("stand")
ex = DataExchange.first()

def count_cards(cards):
    total = 0
    aces = 0
    for c in cards:
        v, r = c.get_current_card()
        if v >= 10 and v < 14:
            total += 10
        elif v == 14:
            total += 11
            aces += 1
        else:
            total += v

        while total > 21 and aces:
            total -= 10
            aces -= 1
    
    return total

while SimEnv.run_main():
    if ex.get_data("player_losses") > 0:
        SimEnvManager.first().reset(stop_code=False)
    sleep(2)
    cards = PlayingCard.find_all()
    player_cards = [card for card in cards if 'player' in card.entity_name]

    sleep(1)

    t = count_cards(player_cards)
    dv, dr = PlayingCard.find("dealer_card1").get_current_card()

    sleep(1)

    if t <= 12:
        hit.press()
        sleep(2)
        t = count_cards(player_cards)
    elif t <= 16 and dv >= 6:
        hit.press()
        sleep(2)
        t = count_cards(player_cards)
    else:
        stand.press()
        sleep(5)

    t = 0
