import re, pandas as pd
from itertools import chain
import time
start = time.time()

maps = []
from_to = {}
f = open('day_5_input.txt')
seeds = [{'min': int(min), 'max': int(min) + int(count)} for (min, count) in re.findall('(\d+) (\d+)', next(f))]

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
locations = []

def getRanges(globalRange, mappings):
    mapEdges = chain(*[[mapping['source_start'], mapping['source_start'] + mapping['length'] - 1] for index, mapping in mappings.iterrows()])
    filteredEdges = set([mapEdge for mapEdge in mapEdges if globalRange['min'] < mapEdge <= globalRange['max']] + [globalRange['min'], globalRange['max']])
    edges = sorted(list(filteredEdges))
    return [{'min': start, 'max': end} for (start, end) in zip(edges[:-1], edges[1:])]

def getLocations(initialRange, initialType):
    type = initialType
    if type == 'location':
        return [initialRange]
    type_df = df[df['from'] == type]
    valueRanges = getRanges(initialRange, type_df)
    locations = []
    for range in valueRanges:
        mappingset = type_df[(type_df['from'] == type) & (type_df['source_start'] <= range['min']) & (type_df['source_start'] + type_df['length'] > range['min'])]
        if not mappingset.empty:
            mapping = mappingset.iloc[0]
            range['min'] +=  (mapping['destination_start'] - mapping['source_start'])
            range['max'] +=  (mapping['destination_start'] - mapping['source_start'])
        locations += getLocations(range, from_to[type])
    return locations

locations = []
for seed in seeds:
    locations += getLocations(seed, 'seed')

locations = sorted(locations, key= lambda v: v['min'], reverse=False)
print(locations[0]['min'])
end = time.time()
print(end - start)

#90168667
#11554135