from pyjop import *

SimEnv.connect()
SimEnvManager.first().reset(stop_code=False)

data = DataExchange.first()
scale = DigitalScale.first()

smiths = data.get_data("goldsmiths")

orders = {smith: float(i + 1) for i, smith in enumerate(smiths)}
data.rpc("order", **orders)
sleep(2)

weight = scale.get_weight()
expected_total = sum(orders.values())
shortage = expected_total - weight

cheater = next(smith for smith, amount in orders.items() 
              if abs(amount * 0.1 - shortage) < 0.0001)

data.rpc("cheater", cheater)
