import copy, math, json
from itertools import chain


matrix = [line.strip() for line in open('day_17_input.txt').readlines()]
width = len(matrix[0])
height = len(matrix)
UP, DOWN, LEFT, RIGHT = (0, -1), (0, 1), (-1, 0), (1, 0)
X, Y = 0, 1

# x,y => loss
# base_cache = dict()

# key is direction, free moves and location.
cache = dict()
final = {'result': {'loss':4000}, 'worst_case_best': (width - 1) * 9 + (height - 1) * 9}
print(width, height, final)
paths = [{'location':(0, 0), 'direction': (0,0), 'straight': 4, 'loss': 0, 'worst_case': final['worst_case_best']}]


def cache_key(path):
    return f"{path['location'][X]},{path['location'][Y]}|{path['direction'][X]},{path['direction'][Y]}|{path['straight']}"

def get_next_steps(path):
    new_paths = []
    for direction in [UP, DOWN, LEFT, RIGHT]:
        new_straight = (path['straight'] + 1) if path['direction'] == direction else 1
        if path['straight'] < 4 and path['direction'] != direction:
            continue
        if new_straight > 10:
            continue
        if direction[X] + path['direction'][X] == 0 and direction[Y] + path['direction'][Y] == 0:
            continue
        new_x = path['location'][X] + direction[X]
        new_y = path['location'][Y] + direction[Y]
        if not (0 <= new_x < width and 0 <= new_y < height):
            continue
        new_path = copy.deepcopy(path)
        new_path['location'] = (new_x, new_y)
        new_path['direction'] = direction
        new_path['loss'] += int(matrix[new_y][new_x])
        new_path['straight'] = new_straight
        
        key = cache_key(new_path)
        value = cache.get(key, False)
        # base_key = f"{new_x},{new_y}"
        # base_value = base_cache.get(base_key, False)
        if value and value <= path['loss']: #or base_value and base_value + 37 <= path['loss']:
            continue
        cache[key] = path['loss']
        # base_cache[base_key] = min(path['loss'], base_cache.get(base_key, path['loss']))
        if final['result'].get('loss', new_path['loss'] + 1) < new_path['loss']:
            continue
        x_remaining = width - new_x - 1
        y_remaining = height - new_y - 1
        best_case = max(x_remaining, math.floor(y_remaining / 3)) * 1 + max(y_remaining, math.floor(x_remaining / 3)) * 1 + new_path['loss']
        worst_case = max(x_remaining, math.floor(y_remaining / 3)) * 9 + max(y_remaining, math.floor(x_remaining / 3)) * 9 + new_path['loss']
        new_path['worst_case'] = worst_case
        if best_case > final['worst_case_best'] + 234:
            continue
        if worst_case < final['worst_case_best']:
            final['worst_case_best'] = worst_case

        if (new_x, new_y) != (width - 1, height -1):
            new_paths.append(new_path)
        elif 4 <= path['straight']:
            print('found a path!', new_path['loss'])
            final['result'] = new_path
        else:
            print('missed end', path)
            continue
    return new_paths

top = 100
counter = 0

while len(paths) > 0:
    new_paths = []
    paths = sorted(paths, key= lambda p: p['loss'])
    for path in paths[:top]:
        new_paths += get_next_steps(path)
    paths = new_paths + paths[top:]
    counter += 1
    if counter % 1000 == 0:
        print('counter', counter, 'path size', len(paths))
        with open('viz_out.txt', 'w') as f:
            f.write(json.dumps([cache]))
print(final)
with open('viz_out.txt', 'w') as f:
    f.write(json.dumps([cache]))
