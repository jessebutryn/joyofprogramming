from pyjop import *
import random

SimEnv.connect()
SimEnvManager.first().reset(stop_code=False)

v = VacuumRobot.first()

movements = []
t = 1

def move_forward(steps):
    for _ in range(steps):
        if v.get_bumper_front():
            return False
        v.move(1)
        movements.append(('move', 1))
        sleep(0.1)
    return True

def turn(direction):
    v.turn(direction)
    movements.append(('turn', direction))
    sleep(0.1)

while SimEnv.run_main():
    if not move_forward(5):
        turn(t)
        if not move_forward(5):
            turn(t)
            t = -t
    else:
        turn(t)
        if not move_forward(5):
            turn(t)
            t = -t

    if random.random() < 0.1:
        t = random.choice([-1, 1])
        turn(t)

    if len(movements) > 1000: 
        break

for action, value in reversed(movements):
    if action == 'move':
        v.move(-value)
    elif action == 'turn':
        v.turn(-value)
    sleep(0.1)

SimEnv.disconnect()
