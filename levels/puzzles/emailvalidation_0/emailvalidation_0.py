from pyjop import *
import re

SimEnv.connect() and SimEnvManager.first().reset(stop_code=False)

e = DataExchange.first()
p = ProximitySensor.first()

pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
ids = []

d = p.get_proximity_data()

for m in p.get_proximity_data():
    if m.entity_name.startswith('id') and not bool(re.match(pattern, m.rfid_tag)):
        ids.append(int(m.entity_name.replace('id', '')))

e.set_data("invalid", ids)
