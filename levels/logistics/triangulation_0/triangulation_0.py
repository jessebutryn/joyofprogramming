from pyjop import *

SimEnv.connect()
SimEnvManager.first().reset(stop_code=False)

env = SimEnvManager.first()

arm = RobotArm.first()
platform = MovablePlatform.find("platform").first()
x = RangeFinder.find("B").get_distance()
y = RangeFinder.find("C").get_distance()  

platform.set_target_location([3.5 + x, 5.3 + y, 0])

arm.set_grabber_location([1.75, 0, 0.5])
sleep(4.5)
arm.pickup()

platform.set_target_location([-1, 5, 0])
arm.set_grabber_location([-2, 0, 4])
sleep(3)
arm.release()

SimEnv.disconnect()
