
from pyvis.network import Network
import networkx as nx
from typing import List

matrix = [line.strip() for line in open('day_23_input.txt').readlines()]
width = len(matrix[0])
height = len(matrix)
UP, DOWN, LEFT, RIGHT = (0, -1), (0, 1), (-1, 0), (1, 0)
X, Y = 0, 1
S = (matrix[0].find('.'), 0)
E = (matrix[height - 1].find('.'), height - 1)
print(S)

DIRS = {
    'UP': UP,
    'DOWN': DOWN,
    'LEFT': LEFT,
    'RIGHT': RIGHT
}

SLOPES = {
    # '^': UP,
    # '>': RIGHT,
    # 'v': DOWN,
    # '<': LEFT
}

longest_path = {'longest': 0}
cache = {} #x, y:[scout_ids]

def cache_add(loc, id):
    x, y = loc
    if x not in cache:
        cache[x] = {y:[id]}
        return True
    if y not in cache[x]:
        cache[x][y] = [id]
        return True
    for val in cache[x][y]:
        if val == id[:len(val)]:
            return False
    cache[x][y].append(id)
    return True

def move(pos, dir):
    return (pos[X] + dir[X], pos[Y] + dir[Y])

def char(pos, matrix):
    x, y = pos
    return matrix[y][x]

def valid(pos, matrix):
    (x, y) = pos
    return 0 <= x < len(matrix[0]) and 0 <= y < len(matrix) and char(pos, matrix) != '#'
        

def get_possible_next_locs(scouts, matrix):
    new_scouts = []
    for scout in scouts:
        if char(scout['loc'], matrix) in SLOPES.keys():
            scout['loc'] = move(scout['loc'], SLOPES[char(scout['loc'], matrix)])
            scout['steps'] += 1
            new_scouts.append(scout)
            continue
        for dir_id, direction in enumerate(DIRS.values()):
            new_loc = move(scout['loc'], direction)
            
            if valid(new_loc, matrix) and cache_add(new_loc, scout['id']):
            
                if new_loc == E:
                    if longest_path['longest'] < scout['steps'] + 1: 
                        longest_path['longest'] = scout['steps'] + 1
                        print('found a path!', longest_path['longest'])
                    continue
                new_scouts.append({'id': scout['id'] + str(dir_id), 'loc': new_loc, 'steps': scout['steps'] + 1})

    return new_scouts

# scouts = [{'id': '1', 'loc': S, 'steps': 0}]
# top = 10
# while len(scouts) > 0:
#     # print('scouts variable: ', scouts[0]['loc'][Y])
#     scouts = sorted(scouts, key=lambda s : (-s['steps'], s['loc'][X], s['loc'][Y]))
#     scouts = scouts[top:] + get_possible_next_locs(scouts[:top], matrix)

# print(longest_path)
# #6300 is too low

# Create a graph out of this.

intersections = {}
for y, row in enumerate(matrix):
    for x, symbol in enumerate(row):
        if symbol == '#':
            continue
        options = [move((x,y), dir) for dir in DIRS.values() if valid(move((x,y), dir), matrix)]
        if len(options) > 2 or (x,y) == S or (x,y) == E:
            intersections[f"{x},{y}"] = options


def get_next_intersection(current, prev, matrix, length = 1):
    options = []
    for dir in DIRS.values():
        new = move(current, dir)
        if new == prev:
            continue
        if valid(new, matrix):
            options.append(new)
    if len(options) > 1:
        return current, length
    if len(options) > 0:
        return get_next_intersection(options[0], current, matrix, length + 1)
    return (-1,-1), -1


edges = []
for key, options in intersections.items():
    xs, ys = key.split(',')
    for option in options:
        loc, weight = get_next_intersection(option, (int(xs), int(ys)), matrix)
        if valid(loc, matrix):
            loc_str = f"{loc[X]},{loc[Y]}"
            edges.append((key, loc_str, weight))
            if (xs, ys) in intersections[loc_str]:
                intersections[loc_str].remove((xs, ys))
            
G = nx.Graph()
for key_from, key_to, weight in edges:
    G.add_edge(key_from, key_to, weight=weight)



def longest_simple_paths(graph, source, target) -> List[List]:
    print('searching path', source, target)
    longest_paths = []
    longest_path_length = 0
    for path in nx.all_simple_paths(G, source=source, target=target):
        path_len = nx.path_weight(graph, path, weight='weight')
        if  path_len > longest_path_length:
            longest_path_length = path_len
            longest_paths.clear()
            longest_paths.append(path)
        elif path_len == longest_path_length:
            longest_paths.append(path)
    return longest_path_length

longest_path = longest_simple_paths(G, source=f"{S[X]},{S[Y]}", target=f"{E[X]},{E[Y]}")
if longest_path:
    print(f"Longest simple path contains {longest_path} nodes")
else:
    print('no path found!')

# Create a network graph using Pyvis
net = Network(height="750px", width="100%", bgcolor="#222222", font_color="white")

# Adding nodes and edges to the Pyvis network
for node in G.nodes:
    net.add_node(node, label=node)

for edge in G.edges:
    net.add_edge(edge[0], edge[1])

# Enabling physics for better layout
net.toggle_physics(True)

# Generating the HTML file
html_file = 'day_23.html'
net.show(html_file, notebook=False)
