from pyjop import *

SimEnv.connect()
SimEnvManager.first().reset(stop_code=False)

car = RaceCar.first()
g = 1
car.set_throttle(1)

while SimEnv.run_main():
    car.set_gear(g)
    sleep(0.1)
    car.apply_boost()
    g = g + 1
    sleep(2)
