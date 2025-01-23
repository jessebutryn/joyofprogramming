from pyjop import *
SimEnv.connect() and SimEnvManager.first().reset(stop_code=False)

v = VacuumRobot.first()

t = 1
while SimEnv.run_main():
    if v.get_bumper_front():
        v.turn(t)
        sleep(0.1)
        for i in range(4):
            v.move(1)
            sleep(0.1)
        v.turn(t)
        t = -t
    else:
        v.move(1)
