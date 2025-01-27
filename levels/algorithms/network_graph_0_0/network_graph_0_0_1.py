from pyjop import *

SimEnv.connect() and SimEnvManager.first().reset(stop_code=False)

edges = [tuple(map(int, x.rfid_tag.split('_')[1:])) for x in SurveillanceSatellite.first().get_satellite_data() if x.rfid_tag.startswith('edge')]

InputBox.find('MaxNode').set_text(max((sum(1 for x in edges if x[0] == n), n) for n in range(max(x[0] for x in edges)))[1])
InputBox.find('WeightSum').set_text(sum(x[2] for x in edges))
InputBox.find('NodeCount').set_text(sum(1 for i in SurveillanceSatellite.first().get_satellite_data() if i.rfid_tag.startswith('node')))
