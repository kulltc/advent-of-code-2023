import pprint

blocks = []
block = []
HORIZONTAL, VERTICAL = 1, 2

def process_block(block):
    block_length = len(block[0])

    for midpoint_left in range(0,block_length):
        smudges = 0
        check_width = min(midpoint_left, block_length - midpoint_left - 2)
        if (check_width < 0):
            break
        for line in block:
            for check in range(0, check_width + 1):
                print(midpoint_left, line, check, line[midpoint_left - check], line[midpoint_left + check + 1])
                if line[midpoint_left - check] != line[midpoint_left + check + 1]:
                    smudges += 1
                if smudges > 1:
                    break
            if smudges > 1:
                break
        if smudges == 1:
            return midpoint_left + 1
    return False

for line in open('day_13_input.txt'):
    line = line.strip()
    if line == '':
        blocks.append(block)
        block = []
        continue
    block.append(line)
blocks.append(block)
score = 0
for block in blocks:
    # pprint.pprint(block)
    result = process_block(block)
    if not result:
        result = 100 * process_block(list(zip(*block)))
    # print('block score', result)
    score += result
print('score', score)