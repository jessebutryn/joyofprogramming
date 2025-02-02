from pyjop import *; import cv2; import numpy as np; SimEnv.connect() and SimEnvManager.first().reset(stop_code=False)

COIN_AREA = { 1: (470, 520), 2: (630, 680), 5: (800, 870), 10: (700, 760), 20: (900, 960), 50: (1050, 1150), 100: (970, 1040), 200: (1180, 1300)}

while SimEnv.run_main():
    sleep(0.2)
    hsv = cv2.cvtColor(SmartCamera.find("cam").get_camera_frame(), cv2.COLOR_RGB2HSV)
    mask = cv2.inRange(hsv, np.array([50, 40, 40]), np.array([80, 255, 255]))
    contours, _ = cv2.findContours(cv2.bitwise_not(mask), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    coins = [coin for cnt in contours for coin in COIN_AREA if COIN_AREA[coin][0] <= cv2.contourArea(cnt) <= COIN_AREA[coin][1]]
    InputBox.first().set_text(sum(coins))
