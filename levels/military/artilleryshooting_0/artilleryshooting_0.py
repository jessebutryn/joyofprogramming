from pyjop import *

SimEnv.connect()
SimEnvManager.first().reset(stop_code=False)

arty = Artillery.first()
v = Vector3()
tg = GPSWaypoint.find("target_center_1m_above")
ag = GPSWaypoint.find("origin")

while SimEnv.run_main():
    t_loc = tg.get_location()
    a_loc = ag.get_location()
    
    target_vector = Vector3(
        t_loc.x - a_loc.x,
        t_loc.y - a_loc.y,
        t_loc.z - a_loc.z
    )

    rotation = v.find_lookat_rotation(target_vector)
    
    distance = ((t_loc.x - a_loc.x)**2 + 
                (t_loc.y - a_loc.y)**2 + 
                (t_loc.z - a_loc.z)**2)**0.5
    
    if distance < 30:
        m = 8.8
    else:
        m = 9.3
    velocity = (distance * m)**0.5
    
    max_pitch = 85
    min_pitch = 45
    max_distance = 100
    
    pitch = max_pitch - (distance/max_distance) * (max_pitch - min_pitch)
    pitch = min(max_pitch, max(min_pitch, pitch))
    
    arty.set_target_rotation(rotation.roll, pitch, rotation.yaw)
    sleep(0.2)
    while arty.get_is_moving():
        sleep(0.1)
    arty.fire(velocity)
    sleep(5)
