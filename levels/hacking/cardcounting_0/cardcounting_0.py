from pyjop import *

SimEnv.connect() and SimEnvManager.first().reset(stop_code=False)

c = PlayingCard.first()
hb = PushButton.find("BetHigh")
lb = PushButton.find("BetLow")
b = InputBox.first()
d = DataExchange.first()

def reset_cards():
    cards = {}
    for i in range(2, 15):
        cards[i] = 4
    return cards

def best_odds(card, cards):
    higher_count = 0
    lower_count = 0

    for rank in range(card + 1, 15):
        higher_count += cards.get(rank, 0)

    for rank in range(2, card):
        lower_count += cards.get(rank, 0)
    
    total_remaining = sum(cards.values())
    
    if total_remaining == 0:
        return (0.5, 0.5)
        
    high_prob = higher_count / total_remaining
    low_prob = lower_count / total_remaining
    
    return (high_prob, low_prob)

i = 0

cards = reset_cards()

while SimEnv.run_main():
    p = d.get_data("Points")
    card, suit = c.get_current_card()
    h, l = best_odds(card, cards)
    if h > 0.9 or l > 0.9:
        bet = p * 0.9
    elif h > .8 or l > .8:
        bet = p * 0.7
    elif h > .75 or l > .75:
        bet = p * 0.3
    elif h > .66 or l > .66:
        bet = p * 0.1
    else:
        bet = p * 0.05

    b.set_text(int(bet))

    if h > l:
        hb.press()
    else:
        lb.press()

    cards[card] -= 1
    i += 1

    if i >= 42:
        cards = reset_cards()
        i = 0

    sleep(1.5)
