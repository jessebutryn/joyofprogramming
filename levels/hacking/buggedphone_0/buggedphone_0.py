from pyjop import *
import numpy as np

SimEnv.connect()

p = DialupPhone.first()

lookups = []
for i in range(10):
    p.dial_number(str(i))
    sleep(1.2)
    lookups.append(p.get_last_number_audio())

SimEnvManager.first().reset(stop_code=False)
sleep(4.5)

n = p.get_last_number_audio()

numbers = []
for i in range(7):
    x = n[i*5909:5909*(i+1)]
    num = str(np.argmin([np.sum(np.abs(y-x)) for y in lookups]))
    numbers.append(num)

p.dial_number("".join(numbers))
