from day_10_viz import create_snake_animation

# x=0,y=0 x=1y=0 x=2,y=0 
# x=0,y=1 x=1,y=1 x=2,y=1
# x=0,y=2 x=1,y=2 x=2,y=2

pipe_types = {
    '|': ((0,-1), (0,1)),
    '-': ((-1,0), (1,0)),
    'L': ((0,-1), (1,0)),
    'J': ((-1,0), (0,-1)),
    '7': ((0,1), (-1,0)),
    'F': ((0, 1), (1,0))
}

pipe_crossing = ['|']

two_part_pipe_crossing = {
    'L':'7',
    'F':'J'
}

connections = {}
s = ()
map = {}

def get_connections(x, y, operations):
    return [f"{x + delta_x},{y + delta_y}" for (delta_x, delta_y) in operations]

def follow(from_point, to_point):
    path = []
    while True:
        path.append(from_point)
        conn = connections.get(to_point)
        if not conn or not from_point in conn:
            return (to_point, path)
        found = conn[0 if conn.index(from_point) == 1 else 1]
        from_point = to_point
        to_point = found
        
def get_tiles_in_loop(path):
    path_matrix = [[] for x in range(y+1)]
    for tile in path:
        tile_x, tile_y = tile.split(',')
        path_matrix[int(tile_y)].append({'x': int(tile_x)})

    count = 0
    for index, row in enumerate(path_matrix):
        row = sorted(row, key=lambda tile: tile['x'])
        prev_x = 0
        currently_inside = False
        part1 = None
        for tile in row:
            char = map[f"{tile['x']},{index}"]
            if currently_inside:
                count += tile['x'] - prev_x - 1
            if char in pipe_crossing:
                currently_inside = not currently_inside
            elif part1 is None and char in two_part_pipe_crossing:
                part1 = char
            elif part1 is not None and char in two_part_pipe_crossing.values():
                if char == two_part_pipe_crossing[part1]:
                    currently_inside = not currently_inside
                part1 = None
            prev_x = tile['x']
    return count

def find_linking_char(before, middle, after):
    before = before.split(',')
    middle = middle.split(',')
    after = after.split(',')
    delta1 = (int(before[0]) - int(middle[0]), int(before[1]) - int(middle[1]))
    delta2 = (int(after[0]) - int(middle[0]), int(after[1]) - int(middle[1]))
    for operator in pipe_types.keys():
        if delta1 in pipe_types[operator] and delta2 in pipe_types[operator]:
            return operator
    
# Build Char Map
for y, line in enumerate(open('day_10_input.txt')):
    for x, char in enumerate(line.strip()):
        map[f"{x},{y}"] = char
        if char == 'S':
            s = (x, y)
        if not char in(pipe_types.keys()):
            continue
        connections[f"{x},{y}"] = get_connections(x, y, pipe_types[char])

# Main loop
start = f"{s[0]},{s[1]}"
for y_offset in range(-1, 2):
    for x_offset in range(-1, 2):
        to = f"{s[0]+x_offset},{s[1]+y_offset}"
        if (x_offset == 0 and y_offset == 0):
            continue
        (end, path) = follow(start, to)
        if (end == start):
            map[f"{s[0]},{s[1]}"] = find_linking_char(path[-1], f"{s[0]},{s[1]}", path[1])
            print (len(path) / 2)
            print (get_tiles_in_loop(path))
            create_snake_animation(y + 1, x + 1, path, [], 'viz.gif')
            exit()
