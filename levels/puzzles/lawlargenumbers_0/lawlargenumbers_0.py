from pyjop import *

SimEnv.connect()
SimEnvManager.first().reset(stop_code=False)

s = ObjectSpawner.first()
cs = TriggerZone.find("CubeScanner")
b = InputBox.first()

r = 0
t = 0

for i in range(10):
    s.spawn()
    sleep(1.7)
    o = cs.get_overlaps()
    for c in o:
        if c.rfid_tag == "Red":
            r += 1
    t = t + len(o)
p = r / t

print(f"percentage: {p}")
b.set_text(p)
