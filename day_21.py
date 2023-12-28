import json

UP, DOWN, LEFT, RIGHT = (0, -1), (0, 1), (-1, 0), (1, 0)
DIRS = {
    'UP': UP,
    'DOWN': DOWN,
    'LEFT': LEFT,
    'RIGHT': RIGHT
}
X, Y = 0, 1
S = ()
EVEN = 0
UNEVEN = 1
source_matrix = [line.strip() for line in open('day_21_input.txt').readlines()]
width = len(source_matrix[0])
height = len(source_matrix)

if width != height:
    exit('width is not height, assumptions broken')
steps = 26501365
start_even_uneven = EVEN if steps % 2 == 0 else UNEVEN

#TODO: check assumption that widht + height steps is sufficient to find all squares in an area when entering from the side.

for y, row in enumerate(source_matrix):
    x = row.find('S')
    if x > -1:
        S = (x,y)
        break

def move(pos, dir):
    return (pos[X] + dir[X], pos[Y] + dir[Y])

def valid(pos, matrix):
    (x, y) = pos
    return 0 <= x < len(matrix[0]) and 0 <= y < len(matrix) and matrix[y][x] != '#' 

def get_possible_next_locs(locs, matrix):
    new_locs = set()
    for loc, mod2 in locs:
        for direction in DIRS.values():
            new_loc = move(loc, direction)
            if valid(new_loc, matrix):
                new_locs.add((new_loc, EVEN if mod2 == EVEN else UNEVEN))
    return new_locs

def negate(even_uneven):
    if even_uneven == EVEN:
        return UNEVEN
    return EVEN


possible_locs = set()
possible_locs.add(((S, EVEN)))
for i in range(width + height + 10):
    possible_locs = get_possible_next_locs(possible_locs, source_matrix)
total = {EVEN:len(possible_locs), UNEVEN:len(get_possible_next_locs(possible_locs, source_matrix))}

import math

full_extra_squares = math.floor(steps / width) - 1
partial_step_mid = int(steps - ((width  - 1) / 2) - full_extra_squares * width)
partial_step_mid_v2 = max(0, int(partial_step_mid - width))

partial_steps_corner = (steps - full_extra_squares * width) if full_extra_squares > 0 else 0
partial_steps_corner_v2 = (steps - (full_extra_squares + 1) * width)

# if even number of full boxes next to the central square, then the last partial box will be ALT
# *|NS|S|NS|S|?

partial_square_even_uneven = negate(start_even_uneven) if full_extra_squares % 2 == 0 else start_even_uneven
partial_square_corner_v2_even_uneven = negate(partial_square_even_uneven) if full_extra_squares > 0 else partial_square_even_uneven
partial_corner_scores = []
partial_corner_scores_v2 = []
partial_mid_scores = []
partial_mid_scores_v2 = []

def run_loc_analysis(source_matrix, partial_steps_corner, start, even_uneven, print_locs = False):
    possible_locs = set()
    x, y = start
    
    possible_locs.add(((x, y), even_uneven))
    result = 0
    for i in range(partial_steps_corner):
        possible_locs = get_possible_next_locs(possible_locs, source_matrix)
        result = len(possible_locs)
    if print_locs:
        open('day_21_1.json', 'w').write(json.dumps(sorted([(loc[0][X], loc[0][Y]) for loc in possible_locs])))
    return result

for s in [(-1,0), (width, 0), (0, height), (width, height-1)]:
    result = run_loc_analysis(source_matrix, partial_steps_corner, s, partial_square_even_uneven)
    partial_corner_scores.append(result)
# v2

for s in [(-1,0), (width, 0), (0, height), (width, height-1)]:
    result = run_loc_analysis(source_matrix, partial_steps_corner_v2, s, partial_square_corner_v2_even_uneven)
    partial_corner_scores_v2.append(result)
   
# minus 1 for 0 based index
midway = int((width + 1) / 2) - 1

for s in [(midway, -1), (midway, height), (-1, midway), (width, midway)]:
    print(s)
    result = run_loc_analysis(source_matrix, partial_step_mid, s, partial_square_even_uneven, s[Y] == -1)
    partial_mid_scores.append(result)


for s in [(midway, -1), (midway, height), (-1, midway), (width, midway)]:
    result = run_loc_analysis(source_matrix, partial_step_mid_v2, s, negate(partial_square_even_uneven))
    partial_mid_scores_v2.append(result)

count = 0
print('count values')
for dir in range(4):
    for w in range(1, full_extra_squares + 1):
        if w % 2 == 0:
            count += total[EVEN] * (w / 2)
            # print(total[EVEN] * (w / 2))
            count += total[UNEVEN] * (w / 2)
            # print(total[UNEVEN] * (w / 2))
        else:
            high = (w + 1) / 2
            low = (w - 1) / 2
            # print ('w', w, 'high', high, 'low', low)
            # print(negate(partial_square_even_uneven))
            count += total[negate(partial_square_even_uneven)] * high
            # print(total[negate(partial_square_even_uneven)] * high)
            count += total[partial_square_even_uneven] * low
            # print(total[partial_square_even_uneven] * low)
    count += partial_mid_scores[dir]
    # print(partial_mid_scores[dir])
    count += (partial_mid_scores_v2[dir] if len(partial_mid_scores_v2) > 0 else 0)
    # print((partial_mid_scores_v2[dir] if len(partial_mid_scores_v2) > 0 else 0))
    count += full_extra_squares * partial_corner_scores[dir]
    # print(full_extra_squares * partial_corner_scores[dir])
    count += (full_extra_squares + 1) * (partial_corner_scores_v2[dir] if len(partial_corner_scores_v2) > 0 else 0)
    # print((full_extra_squares + 1) * (partial_corner_scores_v2[dir] if len(partial_corner_scores_v2) > 0 else 0))
#middle square
count += total[start_even_uneven]
# print(total[start_even_uneven])

print('result', count)
print('full extra', full_extra_squares)
print('total')
print(total)
print('corner')
print(partial_steps_corner)
print(partial_corner_scores, partial_corner_scores_v2)

print('mid')
print(partial_step_mid, partial_step_mid_v2)
print(partial_mid_scores, partial_mid_scores_v2)


# new_matrix = []
# for y, row in enumerate(source_matrix):
#     new_matrix.append(source_matrix[y] + source_matrix[y] + source_matrix[y] + source_matrix[y] + source_matrix[y])
# new_matrix = new_matrix + new_matrix + new_matrix + new_matrix + new_matrix


# possible_locs = set()
# possible_locs.add(((327, 327), EVEN))
# for i in range(steps):
#     possible_locs = get_possible_next_locs(possible_locs, new_matrix)

# print('correct result', len(possible_locs))
# for section_y in range(5):
#     for section_x in range(5):
#         print('section y,x:', section_y, section_x, 'count', len([loc for loc in possible_locs if section_x * width <= loc[0][X] < (section_x + 1) * width and section_y * width <= loc[0][Y] < (section_y + 1) * width]))
#         if section_y == 2 and section_x == 1:
#             open('day_21_2.json', 'w').write(json.dumps(sorted([(loc[0][X] - 131, loc[0][Y] - 262) for loc in possible_locs if section_x * width <= loc[0][X] < (section_x + 1) * width and section_y * width <= loc[0][Y] < (section_y + 1) * width])))

