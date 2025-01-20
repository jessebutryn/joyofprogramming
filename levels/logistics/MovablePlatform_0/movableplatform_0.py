from pyjop import *

SimEnv.connect()
MovablePlatform.first().set_target_location(-1.5,0,8)
MovablePlatform.first().set_target_rotation(0,180,0)
SimEnv.disconnect()
