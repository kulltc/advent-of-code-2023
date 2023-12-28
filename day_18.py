import re, numpy as np

UP, DOWN, LEFT, RIGHT = (0, -1), (0, 1), (-1, 0), (1, 0)
DIRMAP = {
    'U': UP,
    'D': DOWN,
    'L': LEFT,
    'R': RIGHT 
}
HEXDIRMAP = ['R', 'D', 'L', 'U']
X, Y = 0, 1
loc = (0,0)
coords = {0: {0: 'R'}}

for instr in [instr.strip() for instr in open('day_18_input.txt') if instr.strip() != '']:
    dir, len, hex = re.match(r"(\w) (\d+) \(\#(.*)\)", instr).groups()

    dir = HEXDIRMAP[int(hex[5:], 16)]
    len = int(hex[:5], 16)
    if (dir == 'U'):
        coords[loc[Y]][loc[X]] = '*'
    if len < 4:
        for i in range(int(len)):  
            loc = (loc[X] + DIRMAP[dir][X], loc[Y] + DIRMAP[dir][Y])
            row = coords.get(loc[Y], {})
            row[loc[X]] = dir
            coords[loc[Y]] = row
    else:
        loc = (loc[X] + DIRMAP[dir][X], loc[Y] + DIRMAP[dir][Y])
        row = coords.get(loc[Y], {})
        row[loc[X]] = dir
        coords[loc[Y]] = row
    if (dir == 'D'):
        row[loc[X]] = '*'   

min_x = min([min(row.keys()) for row in coords.values()])
max_x = max([max(row.keys()) for row in coords.values()])
min_y = min(coords.keys())
max_y = max(coords.keys())

offset_x = min(min_x, 0) * - 1
offset_y = min(min_y, 0) * - 1

sum = 0

for y, row in sorted(coords.items()):
    inside = False
    last_x = min_x
    for x, type in sorted(row.items()):
        if inside:
            sum += x - last_x #exclude current edge
        else:
            sum += 1 #just count current edge
        if type == '*':
            inside = not inside
        last_x = x

print(sum)

