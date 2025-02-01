# import the joy of programming python module pyjop
from pyjop import *
import cv2
import numpy as np

SimEnv.connect() and SimEnvManager.first().reset(stop_code=False)

for _ in range(6):
    img = SmartCamera.first().get_camera_frame()
    image_bgr = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    hsv_image = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2HSV)
    lower_green = np.array([35, 40, 40])
    upper_green = np.array([85, 255, 255]) 
    mask_green = cv2.inRange(hsv_image, lower_green, upper_green)
    mask_inverted = cv2.bitwise_not(mask_green)
    result = cv2.bitwise_and(image_bgr, image_bgr, mask=mask_inverted)
    binary_image = cv2.threshold(mask_inverted, 1, 255, cv2.THRESH_BINARY)[1]
    contours, _ = cv2.findContours(
        binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )

    InputBox.first().set_text(len(contours))
    sleep(1)
