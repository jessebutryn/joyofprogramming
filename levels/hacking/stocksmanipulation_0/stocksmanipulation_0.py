from pyjop import *

SimEnv.connect() and SimEnvManager.first().reset(stop_code=False)

d = DataExchange.first()

data = d.get_data("PricePrediction")

max_profit = 0
best_buy_day = 0
best_sell_day = 0

for buy_day in range(len(data)):
    for sell_day in range(buy_day + 1, len(data)):
        profit = data[sell_day] - data[buy_day]
        if profit > max_profit:
            max_profit = profit
            best_buy_day = buy_day
            best_sell_day = sell_day

max_stocks = int(1000 / data[best_buy_day])

d.rpc("hold", best_buy_day) 
d.rpc("buy", max_stocks)
d.rpc("hold", best_sell_day - best_buy_day - 1)
d.rpc("sell", max_stocks)
