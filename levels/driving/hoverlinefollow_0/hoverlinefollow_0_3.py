from pyjop import *
import cv2

SimEnv.connect()
SimEnvManager.first().reset(stop_code=False)

base = 20

drone = ServiceDrone.first()

def speed(left, right):
    drone.set_thruster_force_left(left)
    drone.set_thruster_force_right(right)

while SimEnv.run_main():
    img = drone.get_camera_frame()

    center_x = img.shape[1] // 2
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if contours:
        largest = max(contours, key=cv2.contourArea)
        
        M = cv2.moments(largest)
        if M["m00"] != 0:
            cx = int(M["m10"] / M["m00"])
            
            error = center_x - cx
            
            correction = error * 0.1
            
            speed(base - correction, base + correction)
    else:
        speed(base, base)
