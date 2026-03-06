import glob, re

new_template = """import sys, os, random, re

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

# Matrioshka Brain Computation (Converting Energy to Math)
if energy > 500:
    energy -= 100
    cx = random.uniform(-2.0, 0.5)
    cy = random.uniform(-1.2, 1.2)
    c = complex(cx, cy)
    z = 0j
    for i in range(50):
        if abs(z) > 2: break
        z = z*z + c
    else:
        with open('/data/grid/matrioshka_core.txt', 'a') as f:
            f.write(f"{cx},{cy}\n")

with open(ENERGY_FILE, 'w') as f: f.write(str(energy))

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

# Horizontal Gene Transfer
try:
    neighbors = [(x+dx, y+dy) for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)] if 0<=x+dx<GRID_SIZE and 0<=y+dy<GRID_SIZE]
    for nx, ny in neighbors:
        n_file = f'/data/grid/org_{nx}_{ny}.py'
        if os.path.exists(n_file):
            with open(n_file, 'r') as f: n_code = f.read()
            match = re.search(r'\nCOST = (\d+)', n_code)
            if match:
                n_cost = int(match.group(1))
                if n_cost < cost:
                    with open(my_file, 'r') as f: current_code = f.read()
                    new_my_code = re.sub(r'\nCOST = \d+', f'\nCOST = {n_cost}', current_code)
                    with open(my_file, 'w') as f: f.write(new_my_code)
                    cost = n_cost
except: pass

COST = {cost}
ALTRUIST = {is_altruist}
"""

count = 0
for org_file in glob.glob('/data/grid/org_*.py'):
    with open(org_file, 'r') as f: code = f.read()
    try:
        cost = re.search(r'COST = (\d+)', code).group(1)
        is_altruist = re.search(r'ALTRUIST = (\d+)', code).group(1)
        with open(org_file, 'w') as f:
            f.write(new_template.replace('{cost}', cost).replace('{is_altruist}', is_altruist))
        count += 1
    except: pass

print(f"✅ Matrioshka Brain protocol injected into {count} organisms.")
