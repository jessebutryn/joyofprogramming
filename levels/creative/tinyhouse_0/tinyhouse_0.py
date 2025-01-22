from pyjop import *
import numpy as np
SimEnv.connect()
SimEnvManager.first().reset(stop_code=False)

b = VoxelBuilder.first()
e = DataExchange.first()

d = np.array(e.get_data("VoxelTarget"))

for x, y, z in np.ndindex(d.shape):
    if d[x,y,z] == 1:
        b.build_voxel((x,y,z), color=Colors.random())
        sleep(0.1)
