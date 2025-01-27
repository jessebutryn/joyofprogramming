from pyjop import *

SimEnv.connect()
SimEnvManager.first().reset(stop_code=False)

s = SurveillanceSatellite.first()
data = s.get_satellite_data()

node_count = 0
weight_sum = 0
node_edges = {} 

for i in data:
    if i.rfid_tag.startswith('node'):
        node_count += 1
    elif i.rfid_tag.startswith('edge'):
        edge_parts = i.rfid_tag.split('_')
        if len(edge_parts) == 4:
            from_node = int(edge_parts[1])
            weight = int(edge_parts[3])
            node_edges[from_node] = node_edges.get(from_node, 0) + 1
            weight_sum += weight

max_node = max(node_edges.items(), key=lambda x: x[1])[0] if node_edges else 0

InputBox.find('MaxNode').set_text(max_node)
InputBox.find('WeightSum').set_text(weight_sum)
InputBox.find('NodeCount').set_text(node_count)
