from pyjop import *

SimEnv.connect()
SimEnvManager.first().reset(stop_code=False)

drone = ServiceDrone.first()
l, r = 150, 150

def speed(l, r):
    drone.set_thruster_force_left(l)
    drone.set_thruster_force_right(r)

def d_loc():
    l_d = drone.get_distance_left()
    r_d = drone.get_distance_right()
    if l_d > 2.0 and r_d > 2.0:
        return 'off_track'
    elif l_d < 2.0 and r_d < 2.0:
        return 'forward'
    elif l_d > 2.0:
        return 'right'
    elif r_d > 2.0:
        return 'left'

def d(d):
    if d == 'left':
        speed(25, r)
        while d_loc() != 'forward':
            sleep(0.5)
        speed(l, 25)
        sleep(0.75)
    elif d == 'right':
        speed(l, 25)
        while d_loc() != 'forward':
            sleep(0.5)
        speed(25, r)
        sleep(0.75)
    else:
        return
    speed(l, r)

speed(l, r)

while SimEnv.run_main():
    loc = d_loc()
    print(f"Location: {loc}")
    d(loc)    

SimEnv.disconnect()
