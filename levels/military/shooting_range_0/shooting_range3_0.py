from pyjop import *
import numpy as np
import time

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

def calculate_trajectory(detections, prev_detections, delta_time):
    # Calculate trajectory based on image data and previous detections
    for i in detections:
        if i.entity_name.startswith("TargetRed"):
            # Calculate horizontal offset
            horizontal_offset = calc_offset(i.img_left, i.img_width) / 2
            
            # Calculate vertical offset (corrected to aim up)
            vertical_offset = -calc_offset(i.img_top, i.img_height) / 2
            
            # Calculate speed and lead the target
            if len(prev_detections) >= 2:
                prev_i = next((x for x in prev_detections[-2] if x.entity_name == i.entity_name), None)
                if prev_i:
                    speed_x = (i.img_left - prev_i.img_left) / delta_time
                    speed_y = (i.img_top - prev_i.img_top) / delta_time
                    lead_x = speed_x * 0.5  # Adjust lead factor as needed
                    lead_y = speed_y * 0.5  # Adjust lead factor as needed
                    horizontal_offset += lead_x
                    vertical_offset += lead_y
            
            return 0, vertical_offset, horizontal_offset
    return 0, 0, 0

prev_detections = []
prev_time = time.time()
target_detected_time = None

while SimEnv.run_main():
    p.set_target_rotation(0, 15, 0)
    current_time = time.time()
    delta_time = current_time - prev_time
    d = r.get_object_detections()
    img = r.get_camera_frame()
    
    target_detected = any(i.entity_name.startswith("TargetRed") for i in d)
    
    if target_detected:
        if target_detected_time is None:
            target_detected_time = current_time
        elif current_time - target_detected_time > 0.2:  # Wait for 1 second before firing
            if len(prev_detections) >= 2:
                target_rotation = calculate_trajectory(d, prev_detections, delta_time)
                p.set_target_rotation(*target_rotation)
                sleep(0.3)
                r.fire()
    else:
        target_detected_time = None
    
    prev_detections.append(d)
    if len(prev_detections) > 3:
        prev_detections.pop(0)
    prev_time = current_time
    sleep(0.1)
