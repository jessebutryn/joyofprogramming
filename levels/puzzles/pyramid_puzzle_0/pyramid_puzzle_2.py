from pyjop import *

SimEnv.connect()
SimEnvManager.first().reset(stop_code=False)

c = AirliftCrane.first()

c.set_target_location([-3, 0, 2])
sleep(1.2)
c.set_target_location([-3, 0, 0.2])
sleep(1)
c.pickup()
c.set_target_location([-3, 0, 2])
sleep(1)
c.set_target_location([0, 0, 2])
sleep(1.2)
c.set_target_location([0, 0, 0.5])
sleep(1)
c.release()
