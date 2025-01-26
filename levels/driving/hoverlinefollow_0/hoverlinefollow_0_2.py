from pyjop import *
from skimage import color, morphology
from skimage.measure import regionprops, label
from skimage.morphology import remove_small_objects, binary_closing, disk
import cv2
import numpy as np

SimEnv.connect()
SimEnvManager.first().reset(stop_code=False)

drone = ServiceDrone.first()
drone.set_fov(100)
base_speed = 50

lower_line = np.array([80, 50, 150])
upper_line = np.array([200, 255, 255])

def speed(left, right):
    drone.set_thruster_force_left(left)
    drone.set_thruster_force_right(right)

def process_image(image):
    height = image.shape[0]
    bottom_half = image[height//2:, :]
    
    hsv = cv2.cvtColor(bottom_half, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_line, upper_line)
    
    # Enhanced morphological operations
    # First close small gaps
    kernel_small = np.ones((5,5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel_small)
    
    # Then connect vertical gaps with larger kernel
    kernel_vertical = np.ones((15,3), np.uint8)
    mask = cv2.dilate(mask, kernel_vertical, iterations=1)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel_vertical)
    
    # Finally clean up noise
    kernel_clean = np.ones((3,3), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel_clean)
    
    full_mask = np.zeros_like(image[:,:,0])
    full_mask[height//2:, :] = mask

    print(full_mask)
    
    return full_mask

def find_lanes(mask):
    labeled_mask = label(mask)
    regions = regionprops(labeled_mask)
    
    # Get all regions with minimal filtering
    all_centroids = [(region.centroid, region.area) for region in regions if region.area > 200]
    
    if not all_centroids:
        return []
    
    # Split regions into left and right side
    image_center = mask.shape[1] // 2
    left_regions = []
    right_regions = []
    
    for centroid, area in all_centroids:
        if centroid[1] < image_center:
            left_regions.append((centroid, area))
        else:
            right_regions.append((centroid, area))
    
    # Get the largest region from each side
    final_centroids = []
    if left_regions:
        left_centroid = max(left_regions, key=lambda x: x[1])[0]
        final_centroids.append(left_centroid)
    if right_regions:
        right_centroid = max(right_regions, key=lambda x: x[1])[0]
        final_centroids.append(right_centroid)
    
    return final_centroids

def correct_course(centroids, image_width):
    center_x = image_width // 2 
    
    if len(centroids) == 2: 
        left_lane, right_lane = sorted(centroids, key=lambda x: x[1])
        lane_center = (left_lane[1] + right_lane[1]) / 2
        deviation = center_x - lane_center

        print(f"center: {lane_center}, deviation: {deviation}")

        # Smaller threshold for more responsive steering
        if abs(deviation) <= 5:
            return "Stay centered", base_speed, base_speed
        
        # Stronger steering response
        steering_factor = min(abs(deviation) / 50, 0.7)  # Increased from 100 to 50, max from 0.5 to 0.7
        
        # Add minimum steering threshold
        steering_factor = max(steering_factor, 0.2)  # Never steer less than 20%
        
        left_speed = base_speed
        right_speed = base_speed
        
        if deviation > 5:  # Drone is too far left
            right_speed *= (1 - steering_factor)
            print(f"Steering right: reducing right speed to {right_speed}")
        else:  # Drone is too far right
            left_speed *= (1 - steering_factor)
            print(f"Steering left: reducing left speed to {left_speed}")
        
        return f"Steering with factor {steering_factor}", left_speed, right_speed
    else:
        print(f"Both lanes not found")
        return "Stay centered", base_speed, base_speed

while SimEnv.run_main():
    img = drone.get_camera_frame()
    mask = process_image(img)
    centroids = find_lanes(mask)

    action, left_speed, right_speed = correct_course(centroids, img.shape[1])
    print(f"Action: {action}")

    speed(left_speed, right_speed)

SimEnv.disconnect()
