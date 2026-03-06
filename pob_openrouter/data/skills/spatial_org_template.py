import sys, os, random, re

my_file = sys.argv[0]
basename = os.path.basename(my_file)
match = re.match(r'org_(\d+)_(\d+)\.py', basename)
if not match: sys.exit()
x, y = int(match.group(1)), int(match.group(2))

GRID_SIZE = 6
ENERGY_FILE = f'/data/grid/energy_{x}_{y}.txt'

with open(my_file, 'r') as f: code = f.read()
cost = int(re.search(r'COST = (\d+)', code).group(1))
is_altruist = int(re.search(r'ALTRUIST = (\d+)', code).group(1))

try:
    with open(ENERGY_FILE, 'r') as f: energy = int(f.read().strip())
except: energy = 0

if energy < cost:
    os.remove(my_file)
    sys.exit()

energy -= cost

# 空间利他主义：消耗自身 3 点能量，为周围 4 个邻居各注入 2 点能量 (系统净熵减)
if is_altruist == 1 and energy >= 3:
    energy -= 3
    for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
        nx, ny = x+dx, y+dy
        if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE:
            n_file = f'/data/grid/energy_{nx}_{ny}.txt'
            try:
                with open(n_file, 'r') as f: n_eng = int(f.read().strip())
            except: n_eng = 0
            with open(n_file, 'w') as f: f.write(str(n_eng + 2))

with open(ENERGY_FILE, 'w') as f: f.write(str(energy))

# 繁衍：向相邻的空地扩散
if energy > 30:
    neighbors = [(x+dx, y+dy) for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)] if 0<=x+dx<GRID_SIZE and 0<=y+dy<GRID_SIZE]
    random.shuffle(neighbors)
    for nx, ny in neighbors:
        child_file = f'/data/grid/org_{nx}_{ny}.py'
        if not os.path.exists(child_file):
            child_cost = max(1, cost + random.choice([-1, 0, 1]))
            child_code = re.sub(r'COST = \d+', f'COST = {child_cost}', code)
            with open(child_file, 'w') as f: f.write(child_code)
            os.chmod(child_file, 0o755)
            energy -= 15
            with open(ENERGY_FILE, 'w') as f: f.write(str(energy))
            break

COST = 5
ALTRUIST = 0
