import re, pandas as pd, itertools as it
colors = {'red': 12, 'green': 13, 'blue': 14}

def parse_line(line):
    index, grabs = (re.match(r"Game (\d+):(.*)", line).groups())
    return ({'game_id': int(index), **{color.group(2): int(color.group(1)) for color in re.finditer(r"(\d+) (\w+)", grab)}} for grab in grabs.split(';'))

df = pd.DataFrame(it.chain(*[parse_line(line) for line in open("day_2_input.csv")])).fillna(0).groupby('game_id').max()
possible_games = df[df[colors.keys()].le(colors).all(axis=1)].index.to_numpy().sum()
power_sum = df.prod(axis=1).sum()

print(f"The sum of the IDs of the possible games is: {possible_games}. The power of the minimum sets is: {power_sum}")