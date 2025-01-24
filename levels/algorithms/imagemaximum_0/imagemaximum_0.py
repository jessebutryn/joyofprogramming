from pyjop import *
import numpy as np

SimEnv.connect()
SimEnvManager.first().reset(stop_code=False)

img = SmartCamera.first().get_camera_frame()

img_array = np.array(img)
if len(img_array.shape) == 3:
    img_array = np.max(img_array, axis=2)

img_array = (img_array > 128) * 255

section_width = img_array.shape[1] // 10
sections = []

for i in range(10):
    start = i * section_width
    end = (i + 1) * section_width
    section = img_array[:, start:end]
    white_pixels = np.sum(section == 255)
    sections.append(white_pixels)

bar_number = 9 - np.argmax(sections)
InputBox.first().set_text(bar_number)
