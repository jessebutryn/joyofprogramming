from pyjop import *; SimEnv.connect() and SimEnvManager.first().reset(stop_code=False); b = VoxelBuilder.first(); [b.build_voxel((0, 0, n), color=Colors.random()) or sleep(0.1) for n in range(15)]
