from pyjop import *
SimEnv.connect()
SimEnvManager.first().reset(stop_code=False)

r = SniperRifle.first()

while SimEnv.run_main():
    d = r.get_object_detections()
    for i in d:
        if i.entity_name.startswith("TargetRed"):
            r.fire()
