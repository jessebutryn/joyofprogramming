from pyjop import *

SimEnv.connect()
SimEnvManager.first().reset(stop_code=False)

p = MovablePlatform.first()
s = RangeFinder.first()
b = InputBox.first()

f = {}
y = 0
x = 1
nr = 1

for i in range(99):
    t = s.get_rfid_tag()
    if t in f:
        if f[t] > 20:
            b.set_text(t)
            break
        f[t] += 1
    else:
        f[t] = 1
    p.set_target_location(x, y, 0)
    sleep(1)
    if x == 9 and nr:
        y += 1
        x = 9
        nr = 0
    elif x == 0 and nr:
        y += 1
        x = 0
        nr = 0
    elif y % 2 == 0:
        x += 1
        nr = 1
    else:
        x -= 1
        nr = 1
