from pyjop import *
import cv2
import numpy as np
import random

SimEnv.connect() and SimEnvManager.first().reset(stop_code=False)

def get_coin_value(area):
    # Approximate areas for different euro coins (you may need to adjust these values)
    if 500 <= area <= 825: return 1    # 1 cent
    if 825 <= area <= 860: return random.randint(1, 2)
    if 860 <= area <= 950: return 10   # 10 cents
    if 950 <= area <= 1100: return 5    # 5 cents
    if 1100 <= area <= 1250: return 20   # 20 cents
    if 1250 <= area <= 1300: return 50   # 50 cents
    if 1300 <= area <= 1440: return random.choice([50,100])
    if 1440 <= area <= 1700: return 200  # 2 euros
    return 0

while SimEnv.run_main():
    # sleep(0.1)
    img = SmartCamera.first().get_camera_frame()

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Lighter Gaussian blur
    blurred = cv2.GaussianBlur(gray, (1, 1), 2)

    # More precise adaptive thresholding
    thresh = cv2.adaptiveThreshold(
        blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
        cv2.THRESH_BINARY_INV, 25, 3
    )

    # Fill holes in the coins
    height, width = thresh.shape[:2]
    mask = np.zeros((height+2, width+2), np.uint8)
    flood_fill = thresh.copy()
    cv2.floodFill(flood_fill, mask, (0,0), 255)
    flood_fill_inv = cv2.bitwise_not(flood_fill)
    thresh = thresh | flood_fill_inv

    # Smaller kernel for more precise morphology
    kernel = np.ones((3,3), np.uint8)
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=1)
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)

    # Lighter dilation
    thresh = cv2.dilate(thresh, kernel, iterations=1)

    # print(thresh)
    # sleep(2)
    # Find and refine contours
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    refined_contours = []
    
    # Convert to HSV for better color detection
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    for contour in contours:
        # Get the mean color inside the contour
        mask = np.zeros(gray.shape, np.uint8)
        cv2.drawContours(mask, [contour], -1, 255, -1)
        mean_color = cv2.mean(hsv, mask=mask)[:3]
        
        # Adjust area calculation for silver coins (high value in HSV = silver/white)
        area = cv2.contourArea(contour)
        if mean_color[1] < 50 and mean_color[2] > 150:  # Low saturation, high value = silver
            area = area * 0.7  # Reduce detected area for silver coins
            
        epsilon = 0.01 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)
        refined_contours.append((approx, area))  # Store both contour and adjusted area

    # Calculate total value using refined contours
    total_cents = 0
    viz_img = img.copy()

    for contour, adjusted_area in refined_contours:
        value = get_coin_value(adjusted_area)
        total_cents += value

        # Draw contour
        cv2.drawContours(viz_img, [contour], -1, (0, 255, 0), 2)
        
        # Calculate and draw center point
        M = cv2.moments(contour)
        if M["m00"] != 0:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
            cv2.circle(viz_img, (cx, cy), 3, (0, 0, 255), -1)
            cv2.putText(viz_img, f"{int(adjusted_area)}:{value}c", (cx-20, cy-20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

    print(viz_img)  # This will show the image with annotations

    InputBox.first().set_text(total_cents)
    sleep(1)
