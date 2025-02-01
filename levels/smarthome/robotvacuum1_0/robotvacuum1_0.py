from pyjop import *
import random

SimEnv.connect() and SimEnvManager.first().reset(stop_code=False)

v = VacuumRobot.first()

def move_forward():
    steps = 0
    v.move(1)
    sleep(0.1)
    while not v.get_bumper_front():
        steps += 1
        v.move(1)
        sleep(0.1)
    return steps

def turn(direction):
    v.turn(direction)
    sleep(0.1)

while SimEnv.run_main():
    