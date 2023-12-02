import re, inflect
map = {**{inflect.engine().number_to_words(i): i for i in range(1, 10)}, **{str(i): i for i in range(1, 10)}}

def find_number(string, dir):
    return map[re.findall(re.compile(f"({('|'.join(map.keys())[::dir])})"), string[::dir])[0][::dir]]

print(sum((find_number(line, 1) * 10 + find_number(line, -1) for line in open('day_1_input.csv'))))