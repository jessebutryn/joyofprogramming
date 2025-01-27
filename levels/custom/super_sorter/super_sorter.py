from pyjop import *

SimEnv.connect() and SimEnvManager.first().reset(stop_code=False)

scanners = [RangeFinder.find(f"scan{i}") for i in range(4)]
conveyors = [ConveyorBelt.find(f"belt{i}") for i in range(15)]

# # Example: Access individual scanners by index
# first_scanner = scanners[0]
# second_scanner = scanners[1]
# # Get specific readings
# reading0 = scanners[0].get_rfid_tag()
# reading1 = scanners[1].get_rfid_tag()

for c in [10,11,13,14]:
    conveyors[c].set_target_speed(5.0)

def left_move(direction):
    print(f"left_move {direction}")
    if direction == 'left':
        conveyors[9].set_target_speed(5.0)
    elif direction == 'right':
        conveyors[9].set_target_speed(-5.0)
        conveyors[8].set_target_speed(-5.0)
    for c in [2,0,1,6]:
        conveyors[c].set_target_speed(5.0)
    conveyors[3].set_target_speed(-5.0)

    sleep(3)
    conveyors[0].set_target_speed(0.0)
    conveyors[1].set_target_speed(0.0)

def right_move(direction):
    print(f"right_move {direction}")
    if direction == 'left':
        conveyors[9].set_target_speed(5.0)
        conveyors[8].set_target_speed(5.0)
    elif direction == 'right':
        conveyors[8].set_target_speed(-5.0)
    for c in [0,4,5,7]:
        conveyors[c].set_target_speed(5.0)
    conveyors[1].set_target_speed(-5.0)

    sleep(3)
    conveyors[0].set_target_speed(0.0)
    conveyors[1].set_target_speed(0.0)

left_wait = False
right_wait = False


while SimEnv.run_main():
    if scanners[0].get_rfid_tag() == "Box" or scanners[1].get_rfid_tag() == "Box" and not left_wait:
        left_move('left')
    if scanners[1].get_rfid_tag() in ["Cone", "Barrel"] and not left_wait:
        left_move('right')
        left_wait = True
        right_wait = True
    if scanners[0].get_rfid_tag() in ["Cone", "Barrel"] or scanners[2].get_rfid_tag() in ["Cone", "Barrel"] and not right_wait:
        right_move('right')
        right_wait = True
    if scanners[2].get_rfid_tag() == "Box" and not right_wait:
        right_move('left')
        right_wait = True

    if scanners[3].get_rfid_tag() == "Cone":
        conveyors[12].set_target_speed(5.0)
        right_wait = False
        left_wait = False
    elif scanners[3].get_rfid_tag() == "Barrel":
        conveyors[12].set_target_speed(-5.0)
        right_wait = False
        left_wait = False
