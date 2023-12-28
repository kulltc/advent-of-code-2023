import sympy as sp
X, Y, Z = 0, 1, 2

axr,ayr,azr,t = sp.symbols('axr,ayr,azr,t')
bzr,byr,bxr= sp.symbols('bzr,byr,bxr', positive=True, integer=True)

def expand_system(hailstone, system):
    (pos, speed) = hailstone
    bxh, axh = pos[X], speed[X]
    byh, ayh = pos[Y], speed[Y]
    bzh, azh = pos[Z], speed[Z]
    system.append(sp.Eq((bxh - bxr) * (ayr - ayh), (byh - byr) * (axr-axh)))
    system.append(sp.Eq((bxh - bxr) * (azr - azh), (bzh - bzr) * (axr-axh)))

data = []
for line in open('day_24_input.txt'):
    pos, speed = line.strip().split('@')
    pos = [int(pos) for pos in pos.split(',')]
    speed = [int(speed) for speed  in speed.split(',')]
    data.append((pos, speed))

system = []
for hailstone in data:
    expand_system(hailstone, system)

solution = sp.solve(system, [azr,bzr,ayr,byr,axr,bxr])
print(solution)
(sazr,sbzr,sayr,sbyr,saxr,sbxr) = solution[0]
print('solve output', (sazr,sbzr,sayr,sbyr,saxr,sbxr))
print('rock x, y, z', (sbxr,sbyr,sbzr))

