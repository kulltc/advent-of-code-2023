import sympy as sp
X, Y, Z = 0, 1, 2
UPPER_LIMIT = 400000000000000
LOWER_LIMIT = 200000000000000

Y_PER_X, Y_AT_X0, SPEED_Y, POS_Y = 0, 1, 2, 3

# process input
data = []
for line in open('day_24_input.txt'):
    pos, speed = line.strip().split('@')
    pos = [int(pos) for pos in pos.split(',')]
    speed = [int(speed) for speed  in speed.split(',')]
    data.append((pos, speed))

#process data
lines = []
for pos, speed in data:
    y_per_x = speed[Y] / speed[X]
    y_at_x0 = pos[Y] - y_per_x * pos[X]
    t_per_x = 1 / speed[X]
    t_at_x0 = 0 - t_per_x * pos[X]
    lines.append((y_per_x, y_at_x0, speed[Y], pos[Y]))

#intersection
def intersect(A, B):
    if (B[Y_PER_X] - A[Y_PER_X]) == 0:
        return False
    
    x_val = (A[Y_AT_X0]-B[Y_AT_X0]) / (B[Y_PER_X] - A[Y_PER_X])
    y_val = x_val * A[Y_PER_X] + A[Y_AT_X0]

    if LOWER_LIMIT <= x_val <= UPPER_LIMIT and LOWER_LIMIT <= y_val <= UPPER_LIMIT:
        if ((A[SPEED_Y] > 0 and y_val > A[POS_Y]) or (A[SPEED_Y] < 0 and y_val < A[POS_Y])) \
        and ((B[SPEED_Y] > 0 and y_val > B[POS_Y]) or (B[SPEED_Y] < 0 and y_val < B[POS_Y])):
            return True
    return False

# run solution
counter = 0
for index, line1 in enumerate(lines):
    for line2 in lines[index+1:]:
        if intersect(line1, line2):
            counter += 1
print(counter)


