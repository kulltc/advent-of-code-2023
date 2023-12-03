import re, inflect
mapPart1 = {str(i): i for i in range(1, 10)}
mapPart2 = {**mapPart1, **{inflect.engine().number_to_words(i): i for i in range(1, 10)}}

def find_number(string, dir, map):
    return map[re.findall(re.compile(f"({('|'.join(map.keys())[::dir])})"), string[::dir])[0][::dir]]

day1 = lambda map, lines : sum((find_number(line, 1, map) * 10 + find_number(line, -1, map) for line in lines))
print(day1(mapPart1, open('day_1_input.csv').readlines()))
print(day1(mapPart2, open('day_1_input.csv').readlines()))