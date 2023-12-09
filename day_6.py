import math, sympy as sp, re, numpy
timeLine, distanceLine = open('day_6_input.txt').readlines()
hold_time = sp.symbols('hold')

# Let sympy solve "(total_time - hold_time) * hold_time = distance_to_beat"
def algebra(total_time, distance_to_beat):
    min, max = sp.solve(sp.Eq((total_time - hold_time) * hold_time, distance_to_beat))
    return math.ceil(max.evalf()) - math.floor(min.evalf()) - 1

# part 1
times = [int(val) for val in re.findall(r'(\d+)', timeLine)]
distances = [int(val) for val in re.findall(r'(\d+)', distanceLine)]
print(numpy.prod([algebra(time, distance) for time, distance in zip(times, distances)]))

# part 2
time = int(''.join(re.findall(r'(\d+)', timeLine)))
distance = int(''.join(re.findall(r'(\d+)', distanceLine)))
print(algebra(time, distance))
