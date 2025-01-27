from pyjop import *
from collections import defaultdict, deque

SimEnv.connect() and SimEnvManager.first().reset(stop_code=False)

data = SurveillanceSatellite.first().get_satellite_data()
crane = AirliftCrane.first()

graph = defaultdict(list)
node_positions = {}
start = None
end = None

for i in data:
    if i.rfid_tag.startswith('source_node'):
        source_id = i.rfid_tag.split('_')[2] 
        start = source_id
        node_positions[source_id] = i.world_location
    elif i.rfid_tag.startswith('target_node'):
        target_id = i.rfid_tag.split('_')[2]
        end = target_id
        node_positions[target_id] = i.world_location
    elif i.rfid_tag.startswith('edge'):
        edge_parts = i.rfid_tag.split('_')
        if len(edge_parts) >= 4:
            from_node = edge_parts[1]
            to_node = edge_parts[2]
            graph[from_node].append(to_node)
    elif i.rfid_tag.startswith('node'):
        node_id = i.rfid_tag.split('_')[1] 
        node_positions[node_id] = i.world_location

def find_shortest_path(graph, start, end):
    queue = deque([[start]])
    visited = {start}
    
    while queue:
        path = queue.popleft()
        node = path[-1]
        
        if node == end:
            return path
            
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(path + [neighbor])
    return []

path = find_shortest_path(graph, start, end)

for c in path:
    crane.set_target_location(node_positions[c])  # Use the actual Vector3 location
    sleep(0.2)
    while crane.get_is_moving():
        sleep(0.1)
