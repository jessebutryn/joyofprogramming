from pyjop import *
import random

SimEnv.connect()
SimEnvManager.first().set_verbosity_level(verbosity=1)

class DataModel(DataModelBase):
    def __init__(self) -> None:
        super().__init__()
        self.player_next_x = 1.6
        self.dealer_next_x = 1.6
        self.player_cards = []
        self.dealer_cards = []
        self.player_wins = 0
        self.player_losses = 0

data = DataModel()
editor = LevelEditor.first()
editor.select_map(SpawnableMaps.WineCellar)

editor.spawn_static_mesh(SpawnableMeshes.Table, material=SpawnableMaterials.SimpleColor, location=(0, 0, 0), scale=(7, 5, 2), color=Colors.Black)
editor.spawn_static_mesh(SpawnableMeshes.OfficeChair, material=SpawnableMaterials.SimpleColor, location=(0, 3, 0), scale=(3, 3, 2), rotation=(0, 0, 180), color=Colors.Red)

editor.spawn_entity(SpawnableEntities.PushButton, "hit", location=(6.5, -2, 1.5))
editor.spawn_entity(SpawnableEntities.PushButton, "stand", location=(-6.5, -2, 1.5))
editor.spawn_entity(SpawnableEntities.DataExchange, "exchange", location=(8, 0, 0), scale=(2, 2, 2), rotation=(0, 0, -90))

def bj_goal(goal_name: str):
    s = GoalState.Open
    txt = f"Win 3 games of Blackjack. You have won {data.player_wins} so far."

    if data.player_wins >= 3:
        s = GoalState.Success

    editor.set_goal_state(
            "bj_goal",
            s,
            txt
        )
    
    streakgoal = GoalState.Open
    if data.player_losses < 1:
        streakgoal = GoalState.Success
    elif data.player_losses > 0:
        streakgoal = GoalState.Fail
        txt = f"Don't lose any games. You have lost {data.player_losses} games."

    editor.set_goal_state(
        "streak_goal",
        streakgoal,
        f"Don't lose any games. You have lost {data.player_losses} games."
    )

def spawn_card(location, player, face_up=True):
    if player == "player":
        name = f"player_card{len(data.player_cards)}"
        data.player_cards.append(name)
    elif player == "dealer":
        name = f"dealer_card{len(data.dealer_cards)}"
        data.dealer_cards.append(name)

    if face_up:
        editor.spawn_entity(SpawnableEntities.PlayingCard, name, location=location, scale=(20, 20, 5), rotation=(0, 0, 0))
    else:
        editor.spawn_entity(SpawnableEntities.PlayingCard, name, location=location, scale=(20, 20, 5), rotation=(180, 0, 0))
    
    sleep(0.1)
    _ = PlayingCard.find(name).set_card(random.randint(0, 51))
    _ = PlayingCard.find(name).editor_set_has_card_getter(is_enabled=False)
    _ = PlayingCard.find(name).editor_set_has_card_setter(is_enabled=False)

def remove_cards():
    for card in PlayingCard.find_all():
        editor.destroy(card)

    data.player_cards.clear()
    data.dealer_cards.clear()
    data.player_next_x = 1.6
    data.dealer_next_x = 1.6

def deal():
    spawn_card((4, 1, 1.5), "dealer", face_up=False)
    spawn_card((4, -1, 1.5), "player")
    spawn_card((2.8, 1, 1.5), "dealer")
    spawn_card((2.8, -1, 1.5), "player")

def count_cards(player):
    total = 0
    aces = 0
    if player == "player":
        cards = data.player_cards
    elif player == "dealer":
        cards = data.dealer_cards
    for c in cards:
        v, r = PlayingCard.find(c).get_current_card()
        if v >= 10 and v < 14:
            total += 10
        elif v == 14:
            total += 11
            aces += 1
        else:
            total += v

        while total > 21 and aces:
            total -= 10
            aces -= 1
    
    return total

def hit(player):
    if player == "player":
        spawn_card((data.player_next_x, -1, 1.5), "player")
        data.player_next_x -= 1.2
    elif player == "dealer":
        spawn_card((data.dealer_next_x, 1, 1.5), "dealer")
        data.dealer_next_x -= 1.2
    sleep(0.1)
    total = count_cards("player")
    if total > 21:
        print("Player busts!", col = Colors.Red)
        data.player_losses += 1
        
        DataExchange.first().set_data("player_losses", data.player_losses)
        remove_cards()
        sleep(0.1)
        deal()

def player_hit(sender:PushButton,simtime):
    hit("player")

def stand(sender:PushButton,simtime):
    editor.set_rotation("dealer_card0", (-180, 0, 0), 1)
    sleep(1)
    player_total = count_cards("player")
    while count_cards("dealer") < 17:
        hit("dealer")
        sleep(1)
    if count_cards("dealer") > 21 or player_total > count_cards("dealer"):
        print("Player wins!", col = Colors.Green)
        data.player_wins += 1
        DataExchange.first().set_data("player_wins", data.player_wins)
    else:
        print("Dealer wins!", col = Colors.Red)
        data.player_losses += 1
        DataExchange.first().set_data("player_losses", data.player_losses)
    
    remove_cards()
    sleep(0.1)
    deal()

def begin_play():
    on_reset()
    editor.specify_goal("bj_goal", "Win 3 games against the dealer.", bj_goal)
    editor.specify_goal("streak_goal", "Don't lose any games.", None, 0, True, True)
    PushButton.find("hit").on_press(player_hit)
    PushButton.find("stand").on_press(stand)
    sleep(0.1)

def on_reset():
    remove_cards()
    deal()
    data.player_wins = 0
    DataExchange.first().set_data("player_wins", data.player_wins)
    data.player_losses = 0
    DataExchange.first().set_data("player_losses", data.player_losses)

### HINTS CHAT ###
editor.add_hint(0, ["What are the rules of Blackjack?"], "In Blackjack, the goal is to beat the dealer by getting a hand value closer to 21 than the dealer without going over. Face cards (J,Q,K) are worth 10, Aces are worth 1 or 11, and other cards are worth their numerical value.")
editor.add_hint(1, ["How do I win at Blackjack?"], "You win if: 1) Your hand is closer to 21 than the dealer's hand, or 2) The dealer busts (goes over 21). Remember that the dealer must hit on 16 and stand on 17.")
editor.add_hint(2, ["How does the Ace work?"], "An Ace can be worth either 1 or 11. Initially counted as 11, it automatically converts to 1 if counting it as 11 would make your hand go over 21. You can have multiple Aces - they'll adjust automatically to give you the best possible hand.")
editor.add_hint(3, ["What should I do with certain hands?"], """Basic strategy tips:
- Always hit on 11 or below
- Stand on 17 or above
- With 12-16, hit if dealer shows 7 or higher
- Always stand on soft 19 or higher (hand with Ace counted as 11)""")
editor.add_hint(4, ["How does the dealer play?"], "The dealer follows fixed rules: they must hit on 16 or below and must stand on 17 or above. This includes 'soft' 17 (a hand with an Ace counted as 11).")

editor.on_begin_play(begin_play)
editor.on_level_reset(on_reset)
editor.run_editor_level()
