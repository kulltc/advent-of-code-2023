from itertools import chain
matrix = [line.strip() for line in open('day_16_input.txt').readlines()]
width = len(matrix[0])
height = len(matrix)
# print(matrix)


X, Y = 0, 1

def increment(beam, activated, cache):
    char = matrix[beam['pos'][Y]][beam['pos'][X]]
    dirs = []
    if char == '/':
        dirs.append((beam['dir'][Y] * -1, beam['dir'][X] * -1))
    elif char == '\\':
        dirs.append((beam['dir'][Y] * 1, beam['dir'][X] * 1))
    elif char == '|':
        if beam['dir'][X] != 0:
            dirs += [(0,1), (0, -1)]
        else:
            dirs.append(beam['dir'])
    elif char == '-':
        if beam['dir'][Y] != 0:
            dirs += [(1,0), (-1,0)]
        else:
            dirs.append(beam['dir'])
    elif char == '.':
        dirs.append(beam['dir'])
    beams = []
    for dir in dirs:
        new_x = beam['pos'][X] + dir[X]
        new_y = beam['pos'][Y] + dir[Y]
        if  0 <= new_x < width and 0 <= new_y < height and ((new_x, new_y), dir) not in cache:
            beams.append({'pos': (beam['pos'][X] + dir[X], beam['pos'][Y] + dir[Y]), 'dir': dir})
            cache.add(((new_x, new_y), dir))
            activated.add((new_x, new_y))
    return beams

def get_score(start_loc, start_dir):
    activated = set()
    cache = set()
    beams = [{'pos': start_loc, 'dir': start_dir}]
    activated.add(start_loc)
    cache.add((start_loc, start_dir))
    while len(beams) > 0:
        beams = list(chain(*[increment(b, activated, cache) for b in beams]))
    return len(activated)

start_loc, start_dir = (0,0), (1,0)
scores = []

for row in range(0, height):
    scores.append(get_score((0, row), (1, 0)))
    scores.append(get_score((width - 1, row), (-1, 0)))
for column in range(0, width):
    scores.append(get_score((column, 0), (0, 1)))
    scores.append(get_score((column, height - 1), (0, -1)))

print(max(scores))