import re, itertools, math
f = open('day_8_input.txt')
baseInstructions = list(next(f).strip())
positions = []
maps = {}
for line in f:
    if (line.strip() == ''):
       continue
    [key, lr] = [v.strip() for v in line.split('=')]
    left, right = re.findall(r'(\w+)', lr)
    maps[key] = {'L': left, 'R': right, 'Z': True if key[-1] == 'Z' else False}
    if key[-1] == 'A':
        positions.append(key)

def find_pattern (position):
    instr = itertools.cycle(enumerate(baseInstructions))
    pattern = {}
    step = 0
    z_locations = []
    while True:
        instrId, direction = next(instr)
        key = f"{position}|{instrId}"
        if pattern.get(key, False):
            # pattern recurrence found.
            keyPos = list(pattern.keys()).index(key)
            values = list(pattern.values())
            return {
                'base_z':[z for z in z_locations if z < keyPos], 
                'repeat_z':[z - keyPos for z in z_locations if z >= keyPos],
                'repeat_start': keyPos,
                'repeat_length': step - keyPos
            }
        if maps[position]['Z']:
            z_locations.append(step)
        position = maps[position][direction]
        pattern[key] = 1
        step += 1

def getZsInRange(pattern, start, length):
    zs = set()
    if (start <= pattern['repeat_start']):
        zs.update(pattern['base_z'])
    offset = pattern['repeat_start'] + max(0, math.floor((start - pattern['repeat_start']) / pattern['repeat_length'])) * pattern['repeat_length']
    limit = start + length
    while offset <= limit:
        for z in pattern['repeat_z']:
            zs.add(z + offset)
        offset += pattern['repeat_length']
    return zs

patterns = [find_pattern(position) for position in positions] 
for pattern in patterns:
    print(pattern['base_z'], pattern['repeat_z'], pattern['repeat_length'])

current = 0
interval = 10000000000
stop_cond = 0
while not stop_cond:
    print('current: ', current)
    sets = []
    for pattern in patterns:
        sets.append(getZsInRange(pattern, current, interval))
    stop_cond = set.intersection(*sets)
    current += interval
print(min(stop_cond))
exit()



