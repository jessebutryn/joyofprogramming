from pyjop import *
SimEnv.connect()
SimEnvManager.first().reset(stop_code=False)

r = SniperRifle.first()
p = MovablePlatform.first()

def calc_offset(il, iw):
    oc = il + (iw / 2)
    ic = 256 / 2
    po = oc - ic
    dpp = 90 / 256
    a = po * dpp
    if a < 0:
        return a - 2
    else:
        return a + 1

while SimEnv.run_main():
    d = r.get_object_detections()
    for i in d:
        if i.entity_name.startswith("TargetRed"):
            ofs = calc_offset(i.img_left, i.img_width)
            p.set_target_rotation(0,0,ofs/2)
            sleep(2)
            r.fire()
            p.set_target_rotation(0,0,0)
            sleep(1)
