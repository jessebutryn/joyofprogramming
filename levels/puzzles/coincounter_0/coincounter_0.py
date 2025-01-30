from pyjop import *
import cv2
import numpy as np

SimEnv.connect() and SimEnvManager.first().reset(stop_code=False)

for i in range(5):
    img = SmartCamera.first().get_camera_frame()
    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    print(gray)
    
    # Detect circles using Hough Circle Transform
    circles = cv2.HoughCircles(
        gray,
        cv2.HOUGH_GRADIENT,
        dp=1,
        minDist=50,
        param1=60,  # Increased for clearer edges
        param2=35,  # Slightly increased threshold
        minRadius=20,
        maxRadius=100
    )

    print(circles)
    
    coin_count = 0
    if circles is not None:
        circles = np.uint16(np.around(circles))
        coin_count = len(circles[0])
    
    print(f"Number of coins detected: {coin_count}")
