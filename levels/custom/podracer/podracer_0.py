from pyjop import *

SimEnv.connect() and SimEnvManager.first().reset(stop_code=False)

drone = ServiceDrone.first()

moves = [
    {"thrusters": [200, 199], "duration": 10.0, "pulses": 8},
    {"thrusters": [100, 200], "duration": 1.2},
    
    {"thrusters": [200, 200], "duration": 25.0, "pulses": 7},
    {"thrusters": [120, 200], "duration": 3.3},
    
    {"thrusters": [200, 200], "duration": 25.0, "pulses": 6},
    {"thrusters": [180, 120], "duration": 4.7},
    
    {"thrusters": [200, 180], "duration": 25.0, "pulses": 5},
    {"thrusters": [150, 200], "duration": 3.5, "pulses": 1},
    {"thrusters": [160, 200], "duration": 3.5},
    {"thrusters": [200, 200], "duration": 3},
    {"thrusters": [100, 200], "duration": 1.2},
    
    
    {"thrusters": [200, 200], "duration": 25.0, "pulses": 6},
    {"thrusters": [200, 100], "duration": 1.7},
    
    
    {"thrusters": [190, 200], "duration": 25.0, "pulses": 3},
    {"thrusters": [200, 100], "duration": 2.6},
    
    
    {"thrusters": [200, 200], "duration": 25.0, "pulses": 2},
    {"thrusters": [100, 200], "duration": 2.6},
    
    
    {"thrusters": [200, 190], "duration": 25.0, "pulses": 2},
    {"thrusters": [200, 100], "duration": 2.6},
    
    
    {"thrusters": [200, 200], "duration": 25.0, "pulses": 3},
    {"thrusters": [100, 200], "duration": 2.6},
    
    
    {"thrusters": [200, 200], "duration": 25.0, "pulses": 3},
]

while SimEnv.run_main():
    for move in moves:
        drone.set_thruster_force_left(move["thrusters"][0])
        drone.set_thruster_force_right(move["thrusters"][1])
        # sleep(move["duration"])
        if "pulses" in move:
            for _ in range(move["pulses"]):
                drone.apply_thruster_impulse_right(500)
                drone.apply_thruster_impulse_left(500)
                sleep(1)
        else:
            sleep(move["duration"])
