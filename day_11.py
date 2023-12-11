from itertools import chain
f = open('day_11_input.txt')
X, Y = 0, 1

galaxies = list(chain(*[[(x,y) for x, char in enumerate(line) if char == '#'] for y, line in enumerate(f)]))
[rows, columns] = list(zip(*galaxies))
missing = [[val for val in range(min(existing), max(existing)) if val not in set(existing)] for existing in [rows, columns]]
inflation = 1000000 - 1

filter_lt = lambda list, val: [item for item in list if item < val]
galaxies = [(x + len(filter_lt(missing[X], x)) * inflation, y + len(filter_lt(missing[Y], y)) * inflation) for (x,y) in galaxies]
distances = [[abs(x1 - x2) + abs(y1 - y2) for (x2, y2) in galaxies[index + 1:]] for index, (x1, y1) in enumerate(galaxies)]

print(sum(chain(*distances)))