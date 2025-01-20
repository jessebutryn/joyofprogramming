from pyjop import *

SimEnv.connect()

env = SimEnvManager.first()

scanner0 = RangeFinder.find("scan0")
scanner1 = RangeFinder.find("scan1")

for i in [0, 3, 2]:
    ConveyorBelt.find(f"belt{i}").set_target_speed(5.0)

while SimEnv.run_main():
    for _ in range(8):
        scan0_object = ""
        scan1_object = ""
        
        while scan0_object == "":
            scan0_object = scanner0.get_rfid_tag()

        if scan0_object == "Box" or scan0_object == "Cone":
            ConveyorBelt.find("belt1").set_target_speed(5.0)
        elif scan0_object == "Barrel":
            ConveyorBelt.find("belt1").set_target_speed(-5.0)

        scan1_object = scanner1.get_rfid_tag()

        if scan1_object == "Box":
            ConveyorBelt.find("belt4").set_target_speed(-5.0)
        elif scan1_object == "Cone":
            ConveyorBelt.find("belt4").set_target_speed(5.0)

        sleep(7)
        ObjectSpawner.find("spawner").spawn()

SimEnv.disconnect()
