from pyjop import *
from skimage import color, morphology
from skimage.measure import regionprops, label
from skimage.morphology import remove_small_objects, binary_closing, disk
import numpy as np

SimEnv.connect()
SimEnvManager.first().reset(stop_code=False)

drone = ServiceDrone.first()
base_speed = 50

def speed(left, right):
    drone.set_thruster_force_left(left)
    drone.set_thruster_force_right(right)

def process_image(image):
    # Convert image to HSV color space
    hsv_image = color.rgb2hsv(image)
    
    # Extract HSV channels
    hue_channel = hsv_image[..., 0]
    saturation_channel = hsv_image[..., 1]
    value_channel = hsv_image[..., 2]

    # Define yellow mask
    stripes_mask = ((hue_channel <= 0.2) | (hue_channel >= 1.2)) & \
               (saturation_channel >= 0.5) & (value_channel >= 0.3)
    
    cleaned_mask = binary_closing(stripes_mask, disk(3))  # Close gaps
    cleaned_mask = remove_small_objects(cleaned_mask, min_size=50) 
    
    print(cleaned_mask)

    return cleaned_mask

def find_lanes(mask):
    # Label connected components
    labeled_mask = label(mask)

    # Measure region properties and collect centroids
    regions = regionprops(labeled_mask)
    centroids = [region.centroid for region in regions if region.area > 500]
    
    return centroids

def correct_course(centroids, image_width):
    center_x = image_width // 2  # Image center
    
    if len(centroids) == 2:  # Both lanes detected
        left_lane, right_lane = sorted(centroids, key=lambda x: x[1])
        lane_center = (left_lane[1] + right_lane[1]) / 2
        deviation = center_x - lane_center

        print(f"center: {lane_center}, deviation: {deviation}")

        if deviation > 10:  # Drone is too far left
            return "Move right", base_speed, base_speed * 0.5
        elif deviation < -10:  # Drone is too far right
            return "Move left", base_speed * 0.5, base_speed
        else:  # Drone is centered
            return "Stay centered", base_speed, base_speed
    elif len(centroids) == 1:  # One lane detected
        lane_x = centroids[0][1]
        if lane_x < center_x:  # Lane is on the left
            return "Move right", base_speed, base_speed * 0.5
        else:  # Lane is on the right
            return "Move left", base_speed * 0.5, base_speed
    else:  # No lanes detected
        return "Stay centered", base_speed, base_speed

# Main processing loop
while SimEnv.run_main():
    img = drone.get_camera_frame()  # Capture image from drone camera
    
    # Process image to detect lanes
    mask = process_image(img)
    
    # Find lane centroids
    centroids = find_lanes(mask)
    
    # Determine action based on lane positions
    action, left_speed, right_speed = correct_course(centroids, img.shape[1])
    print(f"Action: {action}")
    
    # Adjust drone speed
    speed(left_speed, right_speed)

SimEnv.disconnect()
