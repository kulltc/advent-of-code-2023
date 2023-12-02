import re, inflect
number_mapping = {**{inflect.engine().number_to_words(i): i for i in range(1, 10)}, **{str(i): i for i in range(1, 10)}}

def find_number(string, direction):
    return number_mapping[re.findall(re.compile(f"({('|'.join(number_mapping.keys())[::direction])})"), string[::direction])[0][::direction]]

print(sum((find_number(line, 1) * 10 + find_number(line, -1) for line in open('day_1_input.csv'))))