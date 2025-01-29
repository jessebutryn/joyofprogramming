from pyjop import *
import random

SimEnv.connect()

class DataModel(DataModelBase):
    def __init__(self) -> None:
        super().__init__()
        self.next_x = 2.6

data = DataModel()
editor = LevelEditor.first()
editor.select_map(SpawnableMaps.WineCellar)

editor.spawn_static_mesh(SpawnableMeshes.Table, material=SpawnableMaterials.SimpleColor, location=(0, 0, 0), scale=(7, 5, 1.5), color=Colors.Black)

editor.spawn_entity(SpawnableEntities.PushButton, "hit", location=(6.5, -2, 1.15))
editor.spawn_entity(SpawnableEntities.PushButton, "stay", location=(-6.5, -2, 1.15))


def spawn_card(location, name, face_up=True):
    if face_up:
        editor.spawn_entity(SpawnableEntities.PlayingCard, name, location=location, scale=(20, 20, 5), rotation=(0, 0, 0))
    else:
        editor.spawn_entity(SpawnableEntities.PlayingCard, name, location=location, scale=(20, 20, 5), rotation=(180, 0, 0))
    
    sleep(0.1)
    PlayingCard.find(name).set_card(random.randint(0, 51))
    PlayingCard.find(name).editor_set_has_card_getter(is_enabled=False)
    PlayingCard.find(name).editor_set_has_card_setter(is_enabled=False)

def remove_cards():
    for card in PlayingCard.find_all():
        editor.destroy(card)

def deal():
    spawn_card((5, 1, 1.15), "dealer_card0", face_up=False)
    spawn_card((5, -1, 1.15), "player_card0")
    spawn_card((3.8, 1, 1.15), "dealer_card1")
    spawn_card((3.8, -1, 1.15), "player_card1")

def hit(sender:PushButton,simtime):
    spawn_card((data.next_x, -1, 1.15), f"player_card{len(PlayingCard.find_all())}")
    data.next_x -= 1.2

def begin_play():
    on_reset()
    PushButton.find("hit").on_press(hit)
    # PushButton.find("stay").on_press(stay)

def on_reset():
    remove_cards()
    deal()
    data.next_x = 2.6

editor.on_begin_play(begin_play)
editor.on_level_reset(on_reset)
editor.run_editor_level()
