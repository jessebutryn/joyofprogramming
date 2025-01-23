from pyjop import *
from datetime import datetime

SimEnv.connect()
SimEnvManager.first().reset(stop_code=False)

c = AlarmClock.first()

def get_time():
    now = datetime.now()
    return now.hour + now.minute / 60 + now.second / 3600

c.set_is_running(True)

while SimEnv.run_main():
    c.set_current_time(get_time())

