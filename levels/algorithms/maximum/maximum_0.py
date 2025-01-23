from pyjop import *
SimEnv.connect()
SimEnvManager.first().reset(stop_code=False)

s = RangeFinder.first()
p = MovablePlatform.first()
b = InputBox.first()
th = 0

for n in range(10):
    sleep(1.5)
    h = s.get_size()
    if h.z > th:
        th = h.z
    p.set_target_location(n,0,0)

b.set_text(th)
