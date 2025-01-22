from pyjop import *
SimEnv.connect()
SimEnvManager.first().reset(stop_code=False)

b = VoxelBuilder.first()

for n in range(15):
    b.build_voxel((0,0,n), color=Colors.random())
    sleep(0.1)
