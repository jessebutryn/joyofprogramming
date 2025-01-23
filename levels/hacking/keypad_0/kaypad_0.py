from pyjop import *

SimEnv.connect()
SimEnvManager.first().reset(stop_code=False)

p = PinHacker.first()

low = 0
high = 999

while low <= high:
    mid = (low + high) // 2
    result = p.check_pin(mid)
    sleep(0.5)
    if result == "less":
        low = mid - 1
    elif result == "greater":
        high = mid + 1
    else:
        p.enter_pin(mid)
        break

SimEnv.disconnect()
