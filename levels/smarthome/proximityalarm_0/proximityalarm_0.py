from pyjop import *
SimEnv.connect()
SimEnvManager.first().reset(stop_code=False)

s = ProximitySensor.first()
a = AlarmSiren.first()
d = s.get_proximity_data()

while SimEnv.run_main():
    d = s.get_proximity_data()
    for e in d:
        if e.entity_type == "HumanoidRobot" and e.distance < 2.2:
            a.set_alarm_enabled(True)
