from pyjop import *
SimEnv.connect()
SimEnvManager.first().reset(stop_code=False)

p = MovablePlatform.first()
r = SniperRifle.first()


p.set_target_rotation(0,14,5)

def on_hit(rifle:SniperRifle, gt:float, coll:CollisionEvent):
    print(f"Hit: {coll.entity_name}\n {d}")

positions = []
unique_positions = set()

def is_new_position(new_pos, tolerance=0.1):
    for pos in unique_positions:
        if (abs(pos[0] - new_pos[0]) < tolerance and  # img_left
            abs(pos[1] - new_pos[1]) < tolerance):     # img_top
            return False
    return True

while SimEnv.run_main():
    o = r.get_object_detections()
    for d in o:
        if d.entity_name == "pad":
            pos = (
                round(d.img_left, 1),
                round(d.img_top, 1)
            )
            
            if is_new_position(pos):
                unique_positions.add(pos)
                positions.append({
                    'img_left': pos[0],
                    'img_top': pos[1]
                })
                print(f"\nNew position detected! Total unique positions: {len(unique_positions)}")
                print(f"Position: left={pos[0]}, top={pos[1]}")

#     sleep(0.5)  # Wait before checking again

while SimEnv.run_main():
    o = r.get_object_detections()
    for d in o:
        if d.entity_name == "pad":
            pad_string = f"Pad | img_left: {d.img_left} | img_top: {d.img_top}"
            if d.img_left > 85:
                p.set_target_rotation(0,14,5)
            else:
                p.set_target_rotation(0,14,-5)
        if 'Red' in d.entity_name:   
            r.fire()
            print(pad_string)
            sleep(8)
