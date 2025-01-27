### INIT CODE - DO NOT CHANGE ###
from pyjop import *
import random

SimEnv.connect()
editor = LevelEditor.first()

class DataModel(DataModelBase):
    def __init__(self) -> None:
        super().__init__()
        self.correct = 0
        self.incorrect = 0
        self.seen:Set[str] = set()
        self.last_spawn_at = -999999.0
        
data = DataModel()

conveyors = [
    {"name": "belt0", "location": (-25, 0, 0), "rotation": (0, 0, 0)},
    {"name": "belt1", "location": (-21, 0, 0), "rotation": (0, 0, 90)},
    {"name": "belt2", "location": (-25, 8, 0), "rotation": (0, 0, 0)},
    {"name": "belt3", "location": (-21, 8, 0), "rotation": (0, 0, 90)},
    {"name": "belt4", "location": (-25, -8, 0), "rotation": (0, 0, 0)},
    {"name": "belt5", "location": (-21, -8, 0), "rotation": (0, 0, 90)},
    {"name": "belt6", "location": (-16, 4.0, 0), "rotation": (0, 0, 0), "scale": (2, 1, 1)},
    {"name": "belt7", "location": (-16, -4.0, 0), "rotation": (0, 0, 0), "scale": (2, 1, 1)},
    {"name": "belt8", "location": (-9, -2.5, 0), "rotation": (0, 0, 90), "scale": (1, 1, 1)},
    {"name": "belt9", "location": (-9, 6.5, 0), "rotation": (0, 0, 90), "scale": (2, 1, 1)},
    {"name": "belt10", "location": (-4, 13, 0), "rotation": (0, 0, 0), "scale": (2, 1, 1)},
    {"name": "belt11", "location": (-5.5, -6, 0), "rotation": (0, 0, 0), "scale": (1.5, 1, 1)},
    {"name": "belt12", "location": (0, -6, 0), "rotation": (0, 0, 90), "scale": (2, 1, 1)},
    {"name": "belt13", "location": (2, 1, 0), "rotation": (0, 0, 0), "scale": (1, 1, 1)},
    {"name": "belt14", "location": (2, -13, 0), "rotation": (0, 0, 0), "scale": (1, 1, 1)},
]

scanners = [
    {"name": "scan0", "location": (-18.75, 0, 0.5), "rotation": (0, 0, -90)},
    {"name": "scan1", "location": (-18.75, 8, 0.5), "rotation": (0, 0, -90)},
    {"name": "scan2", "location": (-18.75, -8, 0.5), "rotation": (0, 0, -90)},
    {"name": "scan3", "location": (2, -6, 0.5), "rotation": (0, 0, -90)},
]

spawners = [
    {"name": "spawner0", "location": (-26, 0, 3.5), "rotation": (0, 0, -90)},
    {"name": "spawner1", "location": (-26, 8, 3.5), "rotation": (0, 0, -90)},
    {"name": "spawner2", "location": (-26, -8, 3.5), "rotation": (0, 0, -90)}
]

zones = [
    {"name": "Barrel_Zone", "location": (6.5, 1, 0.8), "scale": 2},
    {"name": "Box_Zone", "location": (4, 13, 0.8), "scale": 2},
    {"name": "Cone_Zone", "location": (6.5, -13, 0.7), "scale": 2}
]

misc = [
    {"name": "Barrel", "location": (6.5, 1, 0.4), "mesh": SpawnableMeshes.BarrelGreen},
    {"name": "Box", "location": (4, 13, 0.3), "mesh": SpawnableMeshes.CardboardBox},
    {"name": "Cone", "location": (6.5, -13, 0.2), "mesh": SpawnableMeshes.TrafficCone}
]

### CONSTRUCTION CODE - Add all code to setup the level (select map, spawn entities) here ###
editor.select_map(SpawnableMaps.BrutalistHall)

for c in conveyors:
    editor.spawn_entity(SpawnableEntities.ConveyorBelt, c["name"], location=c["location"], rotation=c["rotation"], scale=c.get("scale", (1,1,1)))

for s in scanners:
    editor.spawn_entity(SpawnableEntities.RangeFinder, s["name"], location=s["location"], rotation=s["rotation"])
    editor.spawn_static_mesh(SpawnableMeshes.Cube, material=SpawnableMaterials.SimpleColor, location=(s["location"][0], s["location"][1], 0), scale=(0.75, .75, 1), color=Colors.Slategray)

for s in spawners:
    editor.spawn_entity(SpawnableEntities.ObjectSpawner, s["name"], location=s["location"], rotation=s["rotation"])

for z in zones:
    editor.spawn_entity(SpawnableEntities.TriggerZone, z["name"], location=z["location"], scale=z["scale"])

for m in misc:
    editor.spawn_static_mesh(m["mesh"], m["name"], location=m["location"])


def spawn_next():
    if SimEnvManager.first().get_sim_time() - data.last_spawn_at < 5:
        return
    data.last_spawn_at = SimEnvManager.first().get_sim_time()
    i = random.randint(0,2)
    if i == 0:
        spawner = (-26, 0, 3.5)
    elif i == 1:
        spawner = (-26, 8, 3.5)
    elif i == 2:
        spawner = (-26, -8, 3.5)
    i = random.randint(0,2)
    if i == 0:
        editor.spawn_static_mesh(SpawnableMeshes.BarrelGreen, f"Barrel_{random.randint(0,999999)}", rfid_tag = "Barrel", location=spawner, simulate_physics=True, is_temp=True)
    elif i == 1:
        editor.spawn_static_mesh(SpawnableMeshes.CardboardBox, f"Box_{random.randint(0,999999)}", rfid_tag = "Box", location=spawner, simulate_physics=True, is_temp=True)
    elif i == 2:
        editor.spawn_static_mesh(SpawnableMeshes.TrafficCone, f"Cone_{random.randint(0,999999)}", rfid_tag = "Cone", location=spawner, scale = 3, simulate_physics=True, is_temp=True)
### END CONSTRUCTION CODE ###


### GOAL CODE - Define all goals for the player here and implement the goal update functions. ###
def deliver_goal(goal_name: str):
    editor.set_goal_progress(goal_name, data.correct / 8.0, f"Deliver 8 items to their corresponding destinations. Delivered {data.correct}/8")
editor.specify_goal("deliver_goal", "Deliver 8 items to their corresponding destinations.", deliver_goal)

def acc_goal(goal_name: str):
    s = GoalState.Open
    if data.incorrect > 0:
        s = GoalState.Fail
    elif data.correct > 0:
        s = GoalState.Success
    editor.set_goal_state(goal_name, s)
editor.specify_goal("acc_goal", "Don't do any incorrect deliveries.", acc_goal, 0, True, True)

def time_goal(goal_name: str):
    if data.correct >= 10:
        return
    s = GoalState.Open
    t = max(0, 120 - SimEnvManager.first().get_sim_time())
    if t <= 0:
        s = GoalState.Fail
    elif data.correct > 0:
        s = GoalState.Success
    editor.set_goal_state(goal_name, s, f"Finish all deliveries in less than {t:.2f} seconds.")
editor.specify_goal("time_goal", "Finish all deliveries in less than 120 seconds.", time_goal, 0, True, True)
editor.set_goals_intro_text("You need to move items of 3 different categories along these conveyor belts to their correct destination. Only the first item spawns automatically, after that you need to decide when to spawn in the next item using the ObjectSpawner.")
### END GOAL CODE ###


### HINTS CHAT - Define custom hints as question / answer pairs that the player can get answers to via the "AI Ass" chat in-game. ###
editor.add_hint(0,["How do I spawn the next object?", "Nothing is happening after the first object."], "You can manually spawn-in the next object to be delivered. For this simply call the 'spawn' method on the 'ObjectSpawner'. Note: To beat the time limit, you'll need to spawn-in new objects before the delivery of the current one is completed.")
editor.add_hint(1,["Please show me some code to spawn-in the next object.", "How exactly do I spawn the next deliverable item?"], "[#4ABCA5](ObjectSpawner).[#DCDCAA](first)\(\).[#DCDCAA](spawn)\(\)")
### END HINTS ###

### ON BEGIN PLAY CODE - Add any code that should be executed after constructing the level once. ###
def on_deliver(trig:TriggerZone, gt:float, e:TriggerEvent):
    a = e.entity_name.split("_")
    if a and a[0] in ("Box","Barrel","Cone") and e.entity_name not in data.seen:
        data.seen.add(e.entity_name)
        if trig.entity_name.startswith(a[0]):
            data.correct += 1
            col = Colors.Green
        else:
            data.incorrect += 1
            col = Colors.Red
            print(f"Incorrect delivery of {a[0]} at {trig.entity_name}", col=Colors.Orange)
        editor.apply_impulse(e.entity_name, (0,0,20))
        editor.show_vfx(SpawnableVFX.ColorBurst, location = editor.get_location(e.entity_name), color = col)
        editor.play_sound(SpawnableSounds.ExplosionPuff, location = editor.get_location(e.entity_name))
        editor.set_lifetime(e.entity_name, 1.5)

def begin_play():
    print("begin play")
    for r in RangeFinder.find_all():
        r.editor_set_can_read_rfid_tags(True)

    for t in TriggerZone.find_all():
        t.on_triggered(on_deliver)
    on_reset()

editor.on_begin_play(begin_play)
### END ON BEGIN PLAY CODE ###

### ON LEVEL RESET CODE - Add code that should be executed on every level reset. ###
def on_reset():
    print("level resetting")
    data.reset()
    spawn_next()
    # sleep(3)
    # editor.play_camera_sequence([
    #     CameraWaypoint((-5.000,0.000,-1),[0,-85,0],1),
    #     CameraWaypoint((-4.000,0.000,8.500),[0,-85,0],2),
    #     CameraWaypoint((0.000,0.000,8.500),[0,-85,0],1.7),
    #     #CameraWaypoint((0.000,0.000,8.500),[0,-85,90],1),
    #     #CameraWaypoint((0,4.000,8.500),[0,-85,90],2),
    #     CameraWaypoint((0,4.000,8.500),[0,-85,0],1.5),
    #     CameraWaypoint((5.800,4.000,8.500),[0,-85,0],1.3),
    #     #CameraWaypoint((5.800,4.000,8.500),[0,-85,-90],1),
    #     CameraWaypoint((5.800,-0.3,-1.2),[0,-70,-90],0.5)
    # ])

editor.on_level_reset(on_reset)
### END ON LEVEL RESET CODE ###

### ON PLAYER COMMAND CODE - Add code that shoule be executed each time the player issues a code command to an entity
def on_player_command(gametime:float, entity_type:str, entity_name:str, command:str, val:NPArray):
    #print(f"{entity_type=}, {entity_name=}, {command=}")
    if entity_name == "spawner" and command == "Spawn":
        spawn_next()

editor.on_player_command(on_player_command)
### END ON PLAYER COMMAND CODE ###

### LEVEL TICK CODE - Add code that should be executed on every simulation tick. ###

### END LEVEL TICK CODE ###

### EOF CODE - DO NOT CHANGE ###
editor.run_editor_level()
### EOF ###
