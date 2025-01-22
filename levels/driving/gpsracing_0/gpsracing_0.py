from pyjop import *

SimEnv.connect()
SimEnvManager.first().reset(stop_code=False)

w = [Vector3(40,40,0),
    Vector3(40,-40,0),
    Vector3(-40,-40,0),
    Vector3(-40,40,0),]
p = set()

def on_trig(trig:TriggerZone, ts, e):
    p.add(trig.entity_name)

triggers = TriggerZone.find_all()
for t in triggers:
    t.on_triggered(on_trig)

gps = SmartTracker.first()
car = RaceCar.first()
car.set_gear(1)
car.set_throttle(0.5)

while SimEnv.run_main():
    loc = gps.get_location()
    rot = gps.get_rotation()
    wp = w[min(len(p), 3)]

    ta = (rot - loc.find_lookat_rotation(wp)).get_unwinded().yaw

    if car.get_speed() > 10 and abs(ta) > 20:
        car.set_brake(0.5)
        sleep(0.1)
    else:
        car.set_brake(0)

    car.set_steering(clamp(ta/-70,-0.7,0.7))

