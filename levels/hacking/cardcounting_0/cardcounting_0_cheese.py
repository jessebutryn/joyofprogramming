from pyjop import *
SimEnv.connect()

while True:
    rank,points = PlayingCard.first().get_current_card()[0],int(DataExchange.first().get_data("Points"))
    if points == 0 and (SimEnvManager.first().reset(stop_code=False) or True): sleep(1); continue
    InputBox.find("BetAmount").set_text(points)
    PushButton.find("BetHigh").press() if rank < 7 else PushButton.find("BetLow").press()
    sleep(1)
