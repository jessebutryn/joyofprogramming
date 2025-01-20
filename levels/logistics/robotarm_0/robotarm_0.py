from pyjop import *

SimEnv.connect()
SimEnvManager.first().reset(stop_code=False)

arm = RobotArm.first()
arm.set_grabber_location([1.25,0.25,0.5])
sleep(1.8)
arm.pickup()
arm.set_grabber_location([-2.5,0,3])
sleep(1.1)
arm.release()

SimEnv.disconnect()
