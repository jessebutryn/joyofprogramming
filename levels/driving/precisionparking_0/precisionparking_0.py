from pyjop import *

"""
1 impulse = 0.001 meter
102 thruster impulse moves 1 meter
"""

SimEnv.connect()
SimEnvManager.first().reset(stop_code=False)

drone = ServiceDrone.first()
scanner = RangeFinder.first()
dist = scanner.get_distance() - 3.0

def move(power):
    drone.apply_thruster_impulse_left(power)
    drone.apply_thruster_impulse_right(power)

pulses = int(dist // 1)
remainder = dist % 1

for i in range(pulses):
    move(102)

if remainder > 0:
    move(int(remainder * 102))

SimEnv.disconnect()
