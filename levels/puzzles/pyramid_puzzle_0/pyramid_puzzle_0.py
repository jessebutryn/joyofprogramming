from pyjop import *

SimEnv.connect()
SimEnvManager.first().reset(stop_code=False)

c = AirliftCrane.first()

def is_moving():
    sleep(0.2)
    while c.get_is_moving():
        sleep(0.2)

locations = [
    [-3, 0, 1.8],
    [0, 0, 2.5],
    [3, 0, 1.5],
    [3, 0, 2.5],
]

moves = [
    {"l": [-3, 0, 1.8], 'pickup': True},
    {"l": [0, 0, 2.5], 'release': True},
    {"l": [-3, 0, 1.5], 'pickup': True},
    {"l": [-3, 0, 2]},
    {"l": [3, 0, 2.5], 'release': True},
    {"l": [0, 0, 0.5], 'pickup': True},
    {"l": [0, 0, 2]},
    {"l": [3, 0, 2.5], 'release': True},
    {"l": [-3, 0, 0.8], 'pickup': True},
    {"l": [-3, 0, 2]},
    {"l": [0, 0, 2.5], 'release': True},
    {"l": [-3, 0, 1], 'pickup': True},
    {"l": [-3, 0, 2]},
    {"l": [3, 0, 2.5], 'release': True},
    {"l": [-3, 0, 0.5], 'pickup': True},
    {"l": [-3, 0, 2]},
    {"l": [0, 0, 2.5], 'release': True},

]


for m in moves:
    c.set_target_location(m["l"])
    is_moving()
    if m.get("pickup"):
        c.pickup()
    elif m.get("release"):
        c.release()
