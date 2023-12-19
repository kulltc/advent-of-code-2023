
import re

def hash_algo(string):
    current = 0
    for char in string:
        current += ord(char)
        current *= 17
        current = current % 256
    return current


boxes = {}
instructions = [char for char in next(open('day_15_input.txt')).split(',')]
hashes = [hash_algo(instr) for instr in instructions]
print(sum(hashes))


def hash_map(instr):
    label, operation, focal_length = re.match(r'(\w+)([=-])(\d+)?', instr).groups()    
    box_num = hash_algo(label)
    box = boxes.get(box_num, {})
    if operation == '-':
        if label in box:
            del box[label]
    else:
        box[label] = int(focal_length)
    boxes[box_num] = box
    
    
    
for instr in instructions:
    hash_map(instr)
total = 0
for box_num in boxes.keys():
    for count, lens in enumerate(boxes[box_num].values()):
        a = box_num + 1
        b = count + 1
        c = lens
        total += a * b * c
print(total)