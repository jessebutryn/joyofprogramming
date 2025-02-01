from pyjop import *
import cv2
import numpy as np

SimEnv.connect() and SimEnvManager.first().reset(stop_code=False)

SmartCamera.first().set_fov(65)

for i in range(15):
    sleep(2)
    img = SmartCamera.first().get_camera_frame()
    
    # Convert the image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Apply Gaussian blur to the grayscale image
    blurred = cv2.GaussianBlur(gray, (5, 5), 2)
    
    # Use HoughCircles to detect circles in the image
    circles = cv2.HoughCircles(blurred, cv2.HOUGH_GRADIENT, dp=1.5, minDist=20, param1=90, param2=20, minRadius=15, maxRadius=32)
    
    circles = np.round(circles[0, :]).astype("int")
    num_coins = len(circles)
    InputBox.first().set_text(str(num_coins))
