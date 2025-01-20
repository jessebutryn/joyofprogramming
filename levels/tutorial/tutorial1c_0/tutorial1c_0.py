from pyjop import * 

SimEnv.connect()

conveyor = ConveyorBelt.find("_entityConveyorBelt0")
conveyor.set_target_speed(5)
