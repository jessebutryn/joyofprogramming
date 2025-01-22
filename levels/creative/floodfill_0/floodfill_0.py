from pyjop import *
import numpy as np
from scipy.ndimage import label
SimEnv.connect()
SimEnvManager.first().reset(stop_code=False)

b = VoxelBuilder.first()
e = DataExchange.first()

d = np.array(e.get_data("VoxelTarget"))

start_x, start_y = np.argwhere(d == 2)[0]

labeled_array, _ = label(d != 1)
region_label = labeled_array[start_x, start_y]

region_to_fill = (labeled_array == region_label)

rows, cols = d.shape
for x in range(rows):
    for y in range(cols):
        if region_to_fill[x, y]:
            b.build_voxel((x, y, 0), color=(1, 0, 0))
            sleep(0.1)
