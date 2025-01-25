from pyjop import *

SimEnv.connect()
SimEnvManager.first().reset(stop_code=False)

b = PushButton.find("nextA")
s = RangeFinder.find("scanA")
p = MovablePlatform.find("posA")
i = InputBox.first()

tags = []

while True:
    current_tag = s.get_rfid_tag()
    if current_tag in tags:
        break
    tags.append(current_tag)
    b.press()
    sleep(1.2)
    while p.get_is_moving():
        sleep(0.1)

middle_index = len(tags) // 2
middle_tag = tags[middle_index]
i.set_text(middle_tag)