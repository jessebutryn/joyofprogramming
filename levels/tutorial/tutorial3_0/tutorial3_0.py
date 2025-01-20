from pyjop import *

SimEnv.connect()

conveyor = ConveyorBelt.find("_entityConveyorBelt0")
scanner = RangeFinder.find("_entityRangeFinder0")

while SimEnv.run_main():
    scanner = RangeFinder.first()
    tag = scanner.get_rfid_tag()
    if tag == "Box":
        conveyor.set_target_speed(-5.0)
    elif tag == "Barrel":
        conveyor.set_target_speed(5.0)
    else:
        conveyor.set_target_speed(0)
