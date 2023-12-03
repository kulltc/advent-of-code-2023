import pandas as pd, re, itertools as i
pattern = r"(\d+|[^\.\d\n])"
lines = enumerate(open('day_3_input.txt').readlines())

def parseMatch(match, line):
    val =  int(match.group(1)) if match.group(1).isdigit() else None
    stype = 'num' if match.group(1).isdigit() else 'gear' if match.group(1) == '*' else 'part'
    return {'val': val, 'start':match.start(), 'end':match.end()-1, 'line': line, 'type': stype}

def findAdjacent(schematic, row, types):
    return schematic[schematic['type'].isin(types)
        & (schematic['line'] >= row['line'] - 1) & (schematic['line'] <= row['line'] + 1)
        & (schematic['start'] <= row['end'] + 1) & (schematic['end'] >= row['start'] - 1)]    

def gearVal(adjacent):
    return adjacent.product(numeric_only=True)['val'] if len(adjacent) == 2 else 0

schematic = pd.DataFrame(i.chain(*list([parseMatch(m, index) for m in re.finditer(pattern, line)] for index, line in lines)))

#part 1
print(sum([row['val'] for index, row in schematic[schematic['type'] == 'num'].iterrows() if not findAdjacent(schematic, row, ['gear', 'part']).empty]))

# part 2
print(sum(gearVal(findAdjacent(schematic, row, ['num'])) for index, row in schematic[schematic['type'] == 'gear'].iterrows()))
