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

for i in range(len(sizes) - 1):
    min_idx = i
    for j in range(i + 1, len(sizes)):
        if sizes[j]["s"].z < sizes[min_idx]["s"].z:
            min_idx = j
    
    if min_idx != i:
        plata.set_target_location(sizes[i]["x"], 0, 0)
        platb.set_target_location(sizes[min_idx]["x"], 0, 0)
        move_wait()
        
        button.press()
        sleep(0.1)

        temp_x = sizes[i]["x"]
        sizes[i]["x"] = sizes[min_idx]["x"]
        sizes[min_idx]["x"] = temp_x
        sizes[i], sizes[min_idx] = sizes[min_idx], sizes[i]
