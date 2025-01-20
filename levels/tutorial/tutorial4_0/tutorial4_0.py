from pyjop import *

SimEnv.connect()

all_conveyors = ConveyorBelt.find_all()

for conveyor in all_conveyors:
    conveyor.set_target_speed(5.0)
    
SimEnv.disconnect()
