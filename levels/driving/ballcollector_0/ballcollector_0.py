from pyjop import *
from skimage import color
from skimage.measure import regionprops, label

SimEnv.connect()
SimEnvManager.first().reset(stop_code=False)

drone = ServiceDrone.first()

s = 200

def speed(l, r):
    drone.set_thruster_force_left(l)
    drone.set_thruster_force_right(r)

def process_image(image):
    hsv_image = color.rgb2hsv(image)

    green_mask = (hsv_image[..., 0] >= 0.25) & (hsv_image[..., 0] <= 0.4) & \
                 (hsv_image[..., 1] >= 0.4) & (hsv_image[..., 2] >= 0.4)
    red_mask = ((hsv_image[..., 0] >= 0.0) & (hsv_image[..., 0] <= 0.05) | \
                (hsv_image[..., 0] >= 0.95) & (hsv_image[..., 0] <= 1.0)) & \
               (hsv_image[..., 1] >= 0.4) & (hsv_image[..., 2] >= 0.4)
    
    return green_mask, red_mask

def find_ball(mask):
    labeled_mask = label(mask)
    regions = regionprops(labeled_mask)
    if regions:
        largest_region = max(regions, key=lambda region: region.area)
        return largest_region.centroid
    return None

def move_towards(target, image_width):
    center_x = image_width // 2
    
    if target:
        target_x = target[1]
        if target_x < center_x - 10:  # Target is to the left
            speed(s * 0.95, s)
        elif target_x > center_x + 10:  # Target is to the right
            speed(s, s * 0.95)
        else:  # Target is centered
            speed(s, s)
    else:
        speed(0, 0)

while SimEnv.run_main():
    img = drone.get_camera_frame()
    
    green_mask, red_mask = process_image(img)
    
    green_ball = find_ball(green_mask)
    red_ball = find_ball(red_mask)
    
    if green_ball:
        move_towards(green_ball, img.shape[1])
    elif red_ball:
        speed(50, -50) 
    else:
        speed(50, -50) 

SimEnv.disconnect()
