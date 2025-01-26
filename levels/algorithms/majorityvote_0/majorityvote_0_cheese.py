from pyjop import *

SimEnv.connect()
SimEnvManager.first().reset(stop_code=False)

s = RangeFinder.first()
b = InputBox.first()

b.set_text(s.get_rfid_tag())
