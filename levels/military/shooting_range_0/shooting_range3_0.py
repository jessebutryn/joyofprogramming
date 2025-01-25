from pyjop import *
SimEnv.connect()
SimEnvManager.first().reset(stop_code=False)

p = MovablePlatform.first()
r = SniperRifle.first()

while SimEnv.run_main():
    o = r.get_object_detections()
    for d in o:
        if d.entity_name == "pad":
            if d.real_width < 9:
                p.set_target_rotation(0,14,5)
            else:
                p.set_target_rotation(0,14,-5)
        print(d.entity_name)
        if 'Red' in d.entity_name:   
            r.fire()
            sleep(8)
