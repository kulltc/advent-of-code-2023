import re, numpy as np

UP, DOWN, LEFT, RIGHT = (0, -1), (0, 1), (-1, 0), (1, 0)
DIRMAP = {
    'U': UP,
    'D': DOWN,
    'L': LEFT,
    'R': RIGHT 
}
X, Y = 0, 1
loc = (0,0)
coords = {"0,0":"U"}

for instr in [instr.strip() for instr in open('day_18_input.txt') if instr.strip() != '']:
    dir, len, hex = re.match(r"(\w) (\d+) (.*)", instr).groups()
    for i in range(int(len)):
        if (dir == 'U'):
            coords[f"{loc[X]},{loc[Y]}"] = '*'
        loc = (loc[X] + DIRMAP[dir][X], loc[Y] + DIRMAP[dir][Y]) 
        if (dir == 'D'):
            coords[f"{loc[X]},{loc[Y]}"] = '*'
        else:
            coords[f"{loc[X]},{loc[Y]}"] = dir

min_x = min([int(c.split(',')[X]) for c in coords.keys()])
min_y = min([int(c.split(',')[Y]) for c in coords.keys()])
max_y = max([int(c.split(',')[Y]) for c in coords.keys()])
max_x = max([int(c.split(',')[X]) for c in coords.keys()])
offset_x = min(min_x, 0) * - 1
offset_y = min(min_y, 0) * - 1

sum = 0

for y in range(min_y, max_y + 1):
    inside = False
    for x in range(min_x, max_x + 1):
        key = f"{x},{y}"
        if key in coords:

            if coords[key] == '*':
                inside = not inside
            print(x,y)
            sum += 1
        elif inside:
            print(x,y)
            sum += 1


print(sum, coords)

