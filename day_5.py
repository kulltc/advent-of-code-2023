import re, pandas as pd
from itertools import chain
import time
start = time.time()

### -- Parsing input --- ###

maps = []
from_to = {}
f = open('day_5_input.txt')
seedLine = next(f)

for line in f:
    if line.strip() == '':
        continue
    m = re.match(r'(\w+)-to-(\w+) map:', line)
    if (m):
        mapFrom, mapTo = m.groups()
        from_to[mapFrom] = mapTo
    else:
        destinationStart, sourceStart, length = re.match(r'(\d+) (\d+) (\d+)', line).groups()
        maps.append({'from':mapFrom, 'to': mapTo, 'destination_start': int(destinationStart), 'source_start': int(sourceStart), 'length': int(length)})

df = pd.DataFrame(maps)
df['source_end'] = df.source_start + df.length - 1
df['offset'] = df.destination_start - df.source_start
locations = []

def getRanges(globalRange, mappings):
    mapEdges = mappings.source_start.tolist() + mappings.source_end.tolist()
    filteredEdges = set([mapEdge for mapEdge in mapEdges if globalRange['min'] < mapEdge <= globalRange['max']])
    edges = sorted(list(filteredEdges) + [globalRange['min'], globalRange['max']])
    return [{'min': start, 'max': end} for (start, end) in zip(edges[:-1], edges[1:])]

def getLocations(initialRange, initialType):
    type = initialType
    if type == 'location':
        return [initialRange]
    type_df = df[(df['from'] == type) & (df['source_start'].between(initialRange['min'] - 1, initialRange['max'] + 1) 
                                         | df['source_end'].between(initialRange['min'] - 1, initialRange['max'] + 1))]
    valueRanges = getRanges(initialRange, type_df)
    locations = []
    for range in valueRanges:
        mappingset = df[(df['from'] == type) & (df['source_start'] <= range['min']) & (df['source_start'] + df['length'] > range['min'])]
        if not mappingset.empty:
            mapping = mappingset.iloc[0]
            range['min'] +=  mapping.offset
            range['max'] +=  mapping.offset
        locations += getLocations(range, from_to[type])
    return locations

#Part 1
locations = []
for seed in  [{'min': int(seed), 'max': int(seed)} for seed in re.findall('(\d+)', seedLine)]:
    locations += getLocations(seed, 'seed')
locations1 = sorted(locations, key= lambda v: v['min'], reverse=False)

end1 = time.time()
print('part 1', end1 - start)


# Part 2
locations = []
for seed in  [{'min': int(min), 'max': int(min) + int(count)} for (min, count) in re.findall('(\d+) (\d+)', seedLine)]:
    locations += getLocations(seed, 'seed')
locations2 = sorted(locations, key= lambda v: v['min'], reverse=False)

end2 = time.time()
print('part 2', end2 - start)
print(locations1[0]['min'], locations2[0]['min'])
