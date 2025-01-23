from pyjop import *
import cv2
import numpy as np
import time
from collections import deque

SimEnv.connect()
SimEnvManager.first().reset(stop_code=False)

a = AirstrikeControl.first()

target_positions = deque(maxlen=5)

lower_green = np.array([1, 20, 1])
upper_green = np.array([100, 255, 255])

while SimEnv.run_main():
    sleep(1)
    img = a.get_camera_frame()
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_green, upper_green)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if contours:
        min_contour_area = 50
        valid_contours = [cnt for cnt in contours if cv2.contourArea(cnt) > min_contour_area]
        
        if valid_contours:
            target_contour = max(valid_contours, key=cv2.contourArea)
            x, y, w, h = cv2.boundingRect(target_contour)
            target_center = (x + w / 2, y + h / 2)
            
            target_positions.append(target_center)
            
            if len(target_positions) == 5:
                dx = np.mean([target_positions[i][0] - target_positions[i - 1][0] for i in range(1, len(target_positions))])
                dy = np.mean([target_positions[i][1] - target_positions[i - 1][1] for i in range(1, len(target_positions))])
                target_velocity = (dx, dy)
                
                time_step = 1.7
                predicted_position = (target_center[0] + target_velocity[0] * time_step,
                                        target_center[1] + target_velocity[1] * time_step)
                
                img_height, img_width = img.shape[:2]
                normalized_x = predicted_position[0] / img_width
                normalized_y = predicted_position[1] / img_height

                a.launch(normalized_x, normalized_y)
                target_positions.clear()
                sleep(8)
