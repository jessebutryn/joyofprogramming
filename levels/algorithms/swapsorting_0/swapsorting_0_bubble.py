from pyjop import *

SimEnv.connect()
SimEnvManager.first().reset(stop_code=False)

button = PushButton.first()
scana = RangeFinder.find("scanA")
scanb = RangeFinder.find("scanB")
plata = MovablePlatform.find("posA")
platb = MovablePlatform.find("posB")

sizes = []
xpos = 0

def move_wait():
    sleep(0.1)
    while plata.get_is_moving() or platb.get_is_moving():
        sleep(0.1)

for i in range(8):
    plata.set_target_location(xpos, 0, 0)
    move_wait()
    size = scana.get_size()
    sizes.append({"s": size, "x": xpos})
    xpos = xpos + 1

n = len(sizes)
for i in range(n):
    for j in range(0, n-i-1):
        if sizes[j]["s"].z > sizes[j+1]["s"].z:
            plata.set_target_location(sizes[j]["x"], 0, 0)
            platb.set_target_location(sizes[j+1]["x"], 0, 0)
            move_wait()
            
            button.press()
            sleep(0.1)

            temp_x = sizes[j]["x"]
            sizes[j]["x"] = sizes[j+1]["x"]
            sizes[j+1]["x"] = temp_x
            sizes[j], sizes[j+1] = sizes[j+1], sizes[j]
