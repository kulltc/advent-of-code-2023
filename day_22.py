import numpy as np, pandas as pd

X, Y, Z = 0, 1, 2
blocks = []
maxs = {
    X: 0,
    Y: 0,
    Z: 0
}

for line in open('day_22_input.txt'):
    left, right = line.split('~')
    coords_left = list(map(int, left.split(',')))
    coords_right = list(map(int, right.split(',')))
    for k in maxs.keys():
        maxs[k] = max(coords_right[k], maxs[k])
    blocks.append(list(zip(coords_left, coords_right)))
blocks = sorted(blocks, key=lambda b: (b[Z][0], b[Y][0], b[X][0]))

# FIXME: Maybe swap X/Y?
highpoint = np.zeros((maxs[X]+1, maxs[Y]+1))
highpoint_ids = np.zeros((maxs[X]+1, maxs[Y]+1))

supporting_blocks = set()

key_leans_on_val = {key:[] for key in range(1, len(blocks) + 1)}
key_is_leaned_on_by_val = {key:[] for key in range(1, len(blocks) + 1)}

print(key_is_leaned_on_by_val)
a = list({1})
for index, block in enumerate(blocks):
    
    ids = set()
    highest = 0
    for x in range(block[X][0], block[X][1]+1):
        for y in range(block[Y][0], block[Y][1]+1):
            if highpoint[x,y] > highest:
                ids = set()
                ids.add(int(highpoint_ids[x,y]))
                highest = highpoint[x,y]
            if highpoint[x,y] == highest:
                ids.add(int(highpoint_ids[x,y]))
    if highest > 0 and len(ids) == 1:
        supporting_id = list(ids)[0]
        supporting_blocks.add(supporting_id)
    for id in ids:
        if id == 0:
            continue
        key_is_leaned_on_by_val[id].append(index + 1)
        key_leans_on_val[index + 1].append(id)

    highpoint[block[X][0]:block[X][1]+1, block[Y][0]:block[Y][1]+1] = highest + block[Z][1]+1 - block[Z][0]
    highpoint_ids[block[X][0]:block[X][1]+1, block[Y][0]:block[Y][1]+1] = index + 1


print(len(blocks) - len(supporting_blocks))

count = 0

cache = {}
def get_disintegrates(block_id, disintegrated):
    # if block_id in cache:
    #     return cache[block_id]
    count = 0
    for leaner in key_is_leaned_on_by_val[block_id]:
            has_support = False
            for support in key_leans_on_val[leaner]:
                if support not in disintegrated:
                    has_support = True
                    break
            if has_support:
                continue
            else:
                disintegrated.append(leaner)
                count += 1 + get_disintegrates(leaner, disintegrated)
    return count

count = sum(get_disintegrates(block_id, [block_id]) for block_id in range(1, len(blocks) + 1))
        
print(count)