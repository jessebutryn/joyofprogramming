from pyjop import *

SimEnv.connect() and SimEnvManager.first().reset(stop_code=False)

crane = AirliftCrane.find("crane")
instruction_sets = DataExchange.first().get_data("instruction_sets")

def move_crane_to(location):
    crane.set_target_location(location[0], location[1], location[2])
    sleep(0.1)
    while crane.get_is_moving():
        sleep(0.1)

def sim(instructions):
    x, y = 0, 0
    picked_up = False
    for instruction in instructions:
        if instruction == 'L':
            y -= 1
        elif instruction == 'R':
            y += 1
        elif instruction == 'F':
            x += 1
        elif instruction == 'B':
            x -= 1
        elif instruction == 'P':
            pickup_loc = [x, y, 0]
    if x == 0 and y == 0:
        return True, pickup_loc
    else:
        return False, None

for instructions in instruction_sets:
    if 'P' in instructions:
        isvalid, pickup_loc = sim(instructions)
        if isvalid:
            break

move_crane_to(pickup_loc)
crane.pickup()
move_crane_to([0,0,1])
crane.release()
