from pyjop import *
import time

SimEnv.connect()
SimEnvManager.first().reset(stop_code=False)

drone = ServiceDrone.first()
s = 200

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
    
def turn_time():
    s = time.time()
    while d_loc() != 'forward':
        sleep(0.1)
    e = time.time()
    return e - s

def d(d):
    if d == 'left':
        speed(s * 0.33, s * 0.75)
        t = turn_time()
        speed(s, s * 0.5)
        sleep(t * 0.25)
    elif d == 'right':
        speed(s * 0.75, s * 0.33)
        t = turn_time()
        speed(s * 0.5, s)
        sleep(t * 0.25)
    else:
        return
    speed(s, s)

speed(s, s)

while SimEnv.run_main():
    loc = d_loc()
    d(loc)    

SimEnv.disconnect()
