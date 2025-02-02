from pyjop import *

SimEnv.connect()
editor = LevelEditor.first()

editor.select_map(SpawnableMaps.ParkingLot)
editor.set_map_bounds((0, 0, 0), (128, 128, 16))

class DataModel(DataModelBase):
    def __init__(self) -> None:
        super().__init__()
        self.crossed_finish_at = -1.0

data = DataModel()

barriers = [
    {"location": (-33, -32, 0), "rotation": (0, 0, 0)},
    {"location": (-33, -32, 0), "rotation": (0, 0, 90)},
    {"location": (27, -32, 0), "rotation": (0, 0, 0), "scale": (0.085, 1, 1)},
    {"location": (27, 33, 0), "rotation": (0, 0, 0), "scale": (0.085, 1, 1)},
    {"location": (32, -32, 0), "rotation": (0, 0, 90)},
    {"location": (-33, 33, 0), "rotation": (0, 0, 0)},
    {"location": (-33, 28, 0), "rotation": (0, 0, 90), "scale": (0.085, 1, 1)},
    {"location": (32, 28, 0), "rotation": (0, 0, 90), "scale": (0.085, 1, 1)},
    {"location": (-24, -32, 0), "rotation": (0, 0, 90), "scale": (0.95, 1, 1)},
    {"location": (-24, 24.75, 0), "rotation": (0, 0, 0), "scale": (0.75, 1, 1)},
    {"location": (-13, 14, 0), "rotation": (0, 0, 0), "scale": (0.75, 1, 1)},
    {"location": (-24, 2, 0), "rotation": (0, 0, 0), "scale": (0.75, 1, 1)},
    {"location": (-13, -9, 0), "rotation": (0, 0, 0), "scale": (0.75, 1, 1)},
    {"location": (-13, -24, 0), "rotation": (0, 0, 90), "scale": (0.25, 1, 1)},
    {"location": (-4, -32, 0), "rotation": (0, 0, 90), "scale": (0.25, 1, 1)},
    {"location": (5, -24, 0), "rotation": (0, 0, 90), "scale": (0.25, 1, 1)},
    {"location": (16, -32, 0), "rotation": (0, 0, 90), "scale": (0.25, 1, 1)},
]

for barrier in barriers:
    editor.spawn_static_mesh(SpawnableMeshes.ConcreteBarrier, location=barrier['location'], rotation=barrier['rotation'], scale=barrier.get('scale', (1, 1, 1)))

editor.spawn_entity(SpawnableEntities.ServiceDrone, "PodRacer", location=(-29, -28, 1), rotation=(0, 0, 0))
editor.spawn_entity(SpawnableEntities.SmartSpotLight, "finishlight", location=(23, -27, 5), rotation=(0, 10, 0))
editor.spawn_entity(SpawnableEntities.TriggerZone, "finish", location=(23, -28, 0), scale = (12,8,4))

##################
# Goals
##################
def speedo_goal(goal_name: str):
    if data.crossed_finish_at > 0:
        editor.set_goal_state(goal_name,GoalState.Success)
    else:
        editor.set_goal_state(goal_name,GoalState.Open)

def time_goal(goal_name: str):
    TIME_LIMIT = 90.0
    if editor.get_goal_state(goal_name) == GoalState.Success:
        return
    t = max(0,TIME_LIMIT-SimEnvManager.first().get_sim_time())
    msg = f"Finish in under 90 seconds. Time Remaining: {t:.2f}"
    if data.crossed_finish_at > TIME_LIMIT:
        editor.set_goal_state(goal_name,GoalState.Fail, msg)
    elif data.crossed_finish_at > 0:
        editor.set_goal_state(goal_name,GoalState.Success, msg)
    elif t <= 0:
        editor.set_goal_state(goal_name,GoalState.Fail, msg)
    else:
        editor.set_goal_state(goal_name,GoalState.Open, msg)

editor.specify_goal("speedo", "Race around this winding track as fast as possible.", speedo_goal)
editor.specify_goal("time_goal", "Finish in under 90 seconds.", time_goal, 0, True, True)
##################
# End Goals
##################

def on_finish(trigger:TriggerZone, gt:float, dat:TriggerEvent):
    if dat.entity_name == "PodRacer" and data.crossed_finish_at <= 0:
        data.crossed_finish_at = dat.at_time
        light = SmartLight.find("finishlight")
        light.set_color(Colors.Green)
        editor.show_vfx(SpawnableVFX.Fireworks1, location = (23, -28, -5))

def begin_play():
    print("begin play")
    on_reset()

editor.on_begin_play(begin_play)

def on_reset():
    print("level resetting")
    data.reset()
    t = TriggerZone.first()
    t.on_triggered(on_finish)
    SmartLight.find("finishlight").set_color(Colors.Red)
    SmartLight.find("finishlight").set_intensity(50)

editor.on_level_reset(on_reset)

editor.run_editor_level()
