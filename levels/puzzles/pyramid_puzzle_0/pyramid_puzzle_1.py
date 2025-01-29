from pyjop import *

SimEnv.connect()
SimEnvManager.first().reset(stop_code=False)

c = AirliftCrane.first()

def is_moving():
    sleep(0.2)
    while c.get_is_moving():
        sleep(0.2)


moves = [
    {"l": [-3, 0, 2]},
    {"l": [-3, 0, 1.2], 'pickup': True},
    {"l": [-3, 0, 2.2]},
    {"l": [3, 0, 2]},
    {"l": [3,0,1], 'release': True},
    {"l": [0, 0, 2]},
    {"l": [-3, 0, 0.2], 'pickup': True},
    {"l": [-3, 0, 2]},
    {"l": [0, 0, 2]},
    {"l": [0, 0, 1], 'release': True},
    {"l": [3, 0, 2]},
    {"l": [3, 0, 0.2], 'pickup': True},
    {"l": [3, 0, 2]},
    {"l": [0, 0, 2]},
    {"l": [0, 0, 1], 'release': True},
]

for m in moves:
    c.set_target_location(m["l"])
    is_moving()
    if m.get("pickup"):
        c.pickup()
    elif m.get("release"):
        c.release()
        sleep(0.5)
        c.release()
