### INIT CODE - DO NOT CHANGE ###
from pyjop import *

SimEnv.connect()
editor = LevelEditor.first()

### END INIT CODE ###

### CONSTRUCTION CODE - Add all code to setup the level (select map, spawn entities) here ###
editor.select_map(SpawnableMaps.WineCellar)
editor.spawn_entity(SpawnableEntities.DataExchange, "dat", location=(0, 0, 0))

### IMPORTS - Add your imports here ###
import random
### END IMPORTS ###

class DataModel(DataModelBase):
    def __init__(self) -> None:
        super().__init__()
        self.result:str = "-5"
        self.target_fib:int = -12

data = DataModel()

### END CONSTRUCTION CODE ###

### GOAL CODE - Define all goals for the player here and implement the goal update functions. ###
def fib(n:int):
    f_0 = 0
    f_1 = 1
    if n <= 1:
        return n
    for i in range(n-1):
        f_t = f_1
        f_1 = f_0 + f_1
        f_0 = f_t
    return f_1

def fib_goal(goal_name: str):
    s = GoalState.Open
    txt = f"Calculate the Fibonacci number at index [red]({data.target_fib}) and enter the result \(as a string\) in the DataExchange.first() under key 'result'."

    if DataExchange.first().get_data("result") is None:
        s = GoalState.Open
    else:
        if fib := str(DataExchange.first().get_data("result")):
            s = GoalState.Success if fib == data.result else GoalState.Fail

    if s == GoalState.Fail:
        try:
            if not isinstance(DataExchange.first().get_data("result"), str):
                raise JoyfulException()
            if int(DataExchange.first().get_data("result")) > int(data.result):
                txt += " [yellow](Your result is TOO LARGE!)"
            else:
                txt += " [yellow](Your result is too small!)"
        except:
            txt += " [yellow](You have not entered a valid INTEGER as a STRING, e.g. \"53632\")"
    editor.set_goal_state(
        "fib_goal",
        s,
        txt
    )
    if editor.get_goal_state("time_goal") == GoalState.Success:
        return
    stime = GoalState.Open
    if SimEnvManager.first().get_sim_time() > 3.01:
        stime = GoalState.Fail
    elif s == GoalState.Success:
        stime = GoalState.Success
    
    editor.set_goal_state(
        "time_goal",
        stime,
        f"Calculate the result within 3 seconds. {max(0.0,3 - SimEnvManager.first().get_sim_time()):.2f} second remain."
    )

### END GOAL CODE ###

### HINTS CHAT - Define custom hints as question / answer pairs that the player can get answers to via the assistant in-game. ###
editor.add_hint(0,["What is a Fibonacci number?","Please describe the Fibonacci sequence to me."], "In the Fibonacci sequence each number is the sum of the two preceding numbers. Mathematically it is defined as F_i = F_{i-2} + F_{i-1}. Most commonly the sequence starts with F_0 = 0 and F_1 = 1. So the first 10 Fibonacci numbers are 0,1,1,2,3,5,8,13,21,34,... Here is an informative video about it: https://www.youtube.com/watch?v=SjSHVDfXHQ4 ")
editor.add_hint(1,["How can I calculate the Fibonacci sequence in Python?"], "You can calculate the Fibonacci sequence recursively or with an iterative algorithm. What do you prefer?")
editor.add_hint(3,["Recursive."], """[#C586C0](def) [#DCDCAA](fib_rec)\([#9CDCFE](n):[#4ABCA5](int)\)->[#4ABCA5](int):
    [#C586C0](if) [#9CDCFE](n) <= [#B5CEA8](0):
        [#C586C0](return) [#B5CEA8](0)
    [#C586C0](elif) [#9CDCFE](n) == [#B5CEA8](1):
        [#C586C0](return) [#B5CEA8](1)
    [#C586C0](else):
        [#C586C0](return) [#DCDCAA](fib_rec)\([#9CDCFE](n) - [#B5CEA8](1)\) + [#DCDCAA](fib_rec)\([#9CDCFE](n) - [#B5CEA8](2)\)
Please note that, without further optimization, the recursive algorithm has exponential run-time.
""")
editor.add_hint(4,["Please improve the recursive Fibonacci algorithm to have linear run-time instead of exponential run-time."], """You can improve the recursive algorithm by caching all redundant calculation in a dictionary. This process is called memoization and it looks like this:
[#C586C0](def) [#DCDCAA](fib_rec)\([#9CDCFE](n):[#4ABCA5](int), [#9CDCFE](memo)={}\)->[#4ABCA5](int):
    [#C586C0](if) [#9CDCFE](n) <= [#B5CEA8](0):
        [#C586C0](return) [#B5CEA8](0)
    [#C586C0](elif) [#9CDCFE](n) == [#B5CEA8](1):
        [#C586C0](return) [#B5CEA8](1)
    [#C586C0](elif) [#9CDCFE](n) [#C586C0](in) [#9CDCFE](memo):
        [#C586C0](return) [#9CDCFE](memo)[[#9CDCFE](n)]
    [#C586C0](else):
        [#9CDCFE](memo)[[#9CDCFE](n)] = [#DCDCAA](fib_rec)\([#9CDCFE](n) - [#B5CEA8](1), [#9CDCFE](memo)\) + [#DCDCAA](fib_rec)\([#9CDCFE](n) - [#B5CEA8](2), [#9CDCFE](memo)\)
        [#C586C0](return) [#9CDCFE](memo)[[#9CDCFE](n)]
""")
editor.add_hint(6,["Iterative!"], """[#C586C0](def) [#DCDCAA](fibonacci_iterative)\([#9CDCFE](n):[#4ABCA5](int)\)->[#4ABCA5](int):
    [#C586C0](if) [#9CDCFE](n) <= [#B5CEA8](0):
        [#C586C0](return) [#B5CEA8](0)
    [#C586C0](elif) [#9CDCFE](n) == [#B5CEA8](1):
        [#C586C0](return) [#B5CEA8](1)

    [#9CDCFE](prev) = [#B5CEA8](0)
    [#9CDCFE](current) = [#B5CEA8](1)

    [#C586C0](for) [#9CDCFE](i) [#C586C0](in) [#DCDCAA](range)\([#B5CEA8](2), [#9CDCFE](n) + [#B5CEA8](1)\):
        [#9CDCFE](next_fib) = [#9CDCFE](prev) + [#9CDCFE](current)
        [#9CDCFE](prev) = [#9CDCFE](current)
        [#9CDCFE](current) = [#9CDCFE](next_fib)

    [#C586C0](return) [#9CDCFE](current)
""")
editor.add_hint(8, ["Why do I have to enter the result as a string instead of a raw int?"], "The resulting Fibonacci numbers are very large. While python supports arbitrary length integers, the communication protocol between python and the level does not. So to guarantee lossless communication you need to transmit your result as a str instead of an int.")
### END HINTS ###

### ON BEGIN PLAY CODE - Add any code that should be executed after constructing the level once. ###
def begin_play():
    print("begin play")
    on_reset()
    editor.specify_goal("fib_goal", "Calculate the Fibonacci number at index 100 and enter the result in the DataExchange.first() under key 'result'.", fib_goal)
    editor.specify_goal("time_goal", "Calculate the result within 3 seconds.", None, 0, True, True)
    # sleep(3)
    # editor.play_camera_sequence([
    #     CameraWaypoint([6.38,-30.88,2],[0,-15,-60],3),
    #     CameraWaypoint([34.34,-30.88,2],[0,-5,-70],2),
    #     CameraWaypoint([38.34,-31.2,2],[0,-5,23],0.5),
    #     CameraWaypoint([38.34,-1.2,2],[0,-5,23],3)
    # ])

editor.on_begin_play(begin_play)
### END ON BEGIN PLAY CODE ###

### ON LEVEL RESET CODE - Add code that should be executed on every level reset. ###
def on_reset():
    print("level resetting")
    data.target_fib = random.randint(90,110)
    data.result = str(fib(data.target_fib))
    DataExchange.first().set_data("result", None)
    DataExchange.first().set_data("target_fib_idx", data.target_fib)

editor.on_level_reset(on_reset)
### END ON LEVEL RESET CODE ###

### EOF CODE - DO NOT CHANGE ###
editor.run_editor_level()
### EOF ###
