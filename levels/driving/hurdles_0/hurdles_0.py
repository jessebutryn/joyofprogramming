from pyjop import *
SimEnv.connect()
SimEnvManager.first().reset(stop_code=False)

b = HumanoidRobot.first()

b.set_walking(0,1)

while SimEnv.run_main():
    if b.get_is_blocked():
        b.jump()
        sleep(1)

SimEnv.disconnect()
