from pyjop import *

SimEnv.connect()
SimEnvManager.first().reset(stop_code=False)

env = SimEnvManager.first()
car = RaceCar.first()

gear = 1
car.set_throttle(1)
car.set_gear(gear)
car.apply_boost()

while SimEnv.run_main():
    while car.get_rpm() < 7000:
        sleep(0.1)
    gear = gear + 1
    car.set_gear(gear)
    sleep(0.2)
    car.apply_boost()

SimEnv.disconnect()
