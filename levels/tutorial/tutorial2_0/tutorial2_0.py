from pyjop import *

SimEnv.connect()

conveyor = ConveyorBelt.find("_entityConveyorBelt0")
conveyor.set_target_speed(5)

container = DeliveryContainer.find("_entityDeliveryContainer0")
container.open_door()
sleep(6)
container.close_door()
sleep(2.5)

container.deliver()
