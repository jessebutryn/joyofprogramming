from pyjop import *
from skimage import color, morphology
from skimage.measure import regionprops, label
import numpy as np

SimEnv.connect()
SimEnvManager.first().reset(stop_code=False)
drone = ServiceDrone.first()

img = drone.get_camera_frame() 
hsv_image = color.rgb2hsv(img)
hue_channel = hsv_image[..., 0]
saturation_channel = hsv_image[..., 1]
value_channel = hsv_image[..., 2]

stripes_mask = ((hue_channel <= 0.1) | (hue_channel >= 0.9)) & \
               (saturation_channel >= 0.5) & (value_channel >= 0.3)


print(stripes_mask)
