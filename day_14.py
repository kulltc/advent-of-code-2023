
import pprint, math
columns = list(zip(*[line.strip() for line in open('day_14_input.txt').readlines()]))

platform_height = len(columns[0])
platform_width = len(columns)

def get_load(columns):
    load = 0
    for col in columns.values():
        for num in col:
            load += platform_height - num
    return load

matrix = [line.strip() for line in open('day_14_input.txt').readlines()]

roller_coordinates_by_col = {}
block_coordinates_by_col = {}
for y, row in enumerate(matrix):
    for x, char in enumerate(row):
        if char == 'O':
            roller_coordinates_by_col[x] = roller_coordinates_by_col.get(x,[])
            roller_coordinates_by_col[x].append(y)
        elif char == '#':
            block_coordinates_by_col[x] = block_coordinates_by_col.get(x,[])
            block_coordinates_by_col.get(x,[]).append(y)

#y\x 012
#0   abc    gda
#1   def => heb 
#2   ghi    ifc
def rotate_right(coordinates_by_column):
    new_coordinates_by_column = {}
    for x in coordinates_by_column.keys():
        for y in coordinates_by_column[x]:
            new_x = platform_height - y - 1
            new_y = x
            new_coordinates_by_column[new_x] = new_coordinates_by_column.get(new_x, [])
            new_coordinates_by_column[new_x].append(new_y)
    
    for key in new_coordinates_by_column.keys():
        new_coordinates_by_column[key] = sorted(new_coordinates_by_column[key])
    return new_coordinates_by_column

def tilt(block_coordinates_by_col, roller_coordinates_by_col):
    # turn north
    for col in range(0, platform_width):
        new_rollers = []
        for min_c, max_c in zip([-1] + block_coordinates_by_col.get(col,[]), block_coordinates_by_col.get(col, []) + [platform_height]):
            new_rollers += list(range(min_c + 1, min_c + 1 + len([1 for roller in roller_coordinates_by_col.get(col, []) if min_c < roller < max_c])))
        roller_coordinates_by_col[col] = sorted(new_rollers)
    
    return roller_coordinates_by_col

print('load', get_load(tilt(block_coordinates_by_col, roller_coordinates_by_col)))

cache = {}
counter = 0
goal = 1_000_000_000
cache_hit = False

while counter < goal:
    for i in range(4):
        roller_coordinates_by_col = tilt(block_coordinates_by_col, roller_coordinates_by_col)
        roller_coordinates_by_col = rotate_right(roller_coordinates_by_col)
        block_coordinates_by_col = rotate_right(block_coordinates_by_col)
        platform_height, platform_width = platform_width, platform_height
    if not cache_hit:    
        cache_key = "|".join([",".join(str(num) for num in roller_coordinates_by_col[key]) for key in sorted(roller_coordinates_by_col.keys())])
        if (cache_key in cache):
            print("cache_hit")
            jump = counter - cache[cache_key]
            counter += math.floor((goal - counter) / jump) * jump
            cache_hit = True
        else:
            cache[cache_key] = counter
    counter += 1
    
print('load', get_load(roller_coordinates_by_col))