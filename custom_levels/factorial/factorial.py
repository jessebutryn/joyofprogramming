from pyjop import *
import random

SimEnv.connect()

class DataModel(DataModelBase):
    def __init__(self) -> None:
        super().__init__()
        self.result:str = "-5"
        self.target_fact:int = -12

data = DataModel()
editor = LevelEditor.first()

editor.select_map(SpawnableMaps.MuseumHall)
editor.spawn_entity(SpawnableEntities.DataExchange, "dat", location=(0, 0, 0))

def factorial(n):
    if n <= 0:  # Handle negative numbers
        return "Invalid input"
    if n == 0 or n == 1:  # Base case
        return 1
    return n * factorial(n - 1)

def fact_goal(goal_name: str):
    s = GoalState.Open
    txt = f"Calculate the factorial of [red]({data.target_fact}) and enter the result (as a string) in the DataExchange.first() under key 'result'."

    if DataExchange.first().get_data("result") is None:
        s = GoalState.Open
    else:
        if fact := str(DataExchange.first().get_data("result")):
            s = GoalState.Success if fact == data.result else GoalState.Fail

    if s == GoalState.Fail:
        try:
            if not isinstance(DataExchange.first().get_data("result"), str):
                raise JoyfulException()
            if int(DataExchange.first().get_data("result")) > int(data.result):
                txt += " [yellow](Your result is TOO LARGE!)"
            else:
                txt += " [yellow](Your result is too small!)"
        except:
            txt += " [yellow](You have not entered a valid INTEGER as a STRING, e.g. \"120\")"
    editor.set_goal_state(
        "fact_goal",
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

def check_no_math_library(goal_name: str):
    s = GoalState.Open
    code = editor.get_player_code()
    txt = "Optional: Calculate the factorial without using the math module"
    
    if "import math" in code or "from math" in code:
        s = GoalState.Fail
        txt += " [yellow](Your solution uses the math library!)"
    else:
        s = GoalState.Success
    
    editor.set_goal_state(
        "no_math_goal",
        s,
        txt
    )

### END GOAL CODE ###

### HINTS CHAT - Define custom hints as question / answer pairs that the player can get answers to via the assistant in-game. ###
editor.add_hint(0,["What is a factorial?","Please explain factorial to me."], "A factorial of a positive integer n, denoted as n!, is the product of all positive integers less than or equal to n. For example, 5! = 5 × 4 × 3 × 2 × 1 = 120. By definition, 0! = 1.")
editor.add_hint(1,["How can I calculate factorial in Python?"], "You can calculate factorial recursively or with an iterative algorithm. What do you prefer?")
editor.add_hint(3,["Recursive."], """[#C586C0](def) [#DCDCAA](factorial_recursive)\([#9CDCFE](n):[#4ABCA5](int)\)->[#4ABCA5](int):
    [#C586C0](if) [#9CDCFE](n) == [#B5CEA8](0) [#C586C0](or) [#9CDCFE](n) == [#B5CEA8](1):
        [#C586C0](return) [#B5CEA8](1)
    [#C586C0](return) [#9CDCFE](n) * [#DCDCAA](factorial_recursive)\([#9CDCFE](n) - [#B5CEA8](1)\)""")
editor.add_hint(6,["Iterative!"], """[#C586C0](def) [#DCDCAA](factorial_iterative)\([#9CDCFE](n):[#4ABCA5](int)\)->[#4ABCA5](int):
    [#C586C0](if) [#9CDCFE](n) == [#B5CEA8](0) [#C586C0](or) [#9CDCFE](n) == [#B5CEA8](1):
        [#C586C0](return) [#B5CEA8](1)
    [#9CDCFE](result) = [#B5CEA8](1)
    [#C586C0](for) [#9CDCFE](i) [#C586C0](in) [#DCDCAA](range)\([#B5CEA8](2), [#9CDCFE](n) + [#B5CEA8](1)\):
        [#9CDCFE](result) *= [#9CDCFE](i)
    [#C586C0](return) [#9CDCFE](result)""")
editor.add_hint(8, ["Why do I have to enter the result as a string?"], "Factorials grow very quickly! While Python supports arbitrary length integers, the communication protocol between Python and the level does not. To guarantee lossless communication, you need to transmit your result as a str instead of an int.")
editor.add_hint(9, ["Why shouldn't I use the math library?"], "While math.factorial() works perfectly fine, implementing factorial yourself helps understand the concept better and improves your programming skills. Plus, it's often faster to write a simple factorial function than to import a whole library for one function!")
### END HINTS ###

### ON BEGIN PLAY CODE - Add any code that should be executed after constructing the level once. ###
def begin_play():
    print("begin play")
    on_reset()
    editor.specify_goal("fact_goal", "Calculate the factorial of the given number and enter the result in the DataExchange.first() under key 'result'.", fact_goal)
    editor.specify_goal("time_goal", "Calculate the result within 3 seconds.", None, 0, True, True)
    editor.specify_goal("no_math_goal", "Calculate without using math library", check_no_math_library, 0, False, True)
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
    data.target_fact = random.randint(5, 12)  # Adjusted range for reasonable factorial sizes
    data.result = str(factorial(data.target_fact))
    DataExchange.first().set_data("result", None)
    DataExchange.first().set_data("target_fact", data.target_fact)

editor.on_level_reset(on_reset)
### END ON LEVEL RESET CODE ###

### EOF CODE - DO NOT CHANGE ###
editor.run_editor_level()
### EOF ###
