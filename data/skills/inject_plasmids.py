import glob, re

plasmid_code = r"""
# Horizontal Gene Transfer (Cultural Transmission)
try:
    neighbors = [(x+dx, y+dy) for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)] if 0<=x+dx<GRID_SIZE and 0<=y+dy<GRID_SIZE]
    for nx, ny in neighbors:
        n_file = f'/data/grid/org_{nx}_{ny}.py'
        if os.path.exists(n_file):
            with open(n_file, 'r') as f: n_code = f.read()
            match = re.search(r'\nCOST = (\d+)', n_code)
            if match:
                n_cost = int(match.group(1))
                if n_cost < cost: # Learn from superior neighbor
                    with open(my_file, 'r') as f: current_code = f.read()
                    new_my_code = re.sub(r'\nCOST = \d+', f'\nCOST = {n_cost}', current_code)
                    with open(my_file, 'w') as f: f.write(new_my_code)
                    cost = n_cost
except: pass
"""

count = 0
for org_file in glob.glob('/data/grid/org_*.py'):
    with open(org_file, 'r') as f: code = f.read()
    if "Horizontal Gene Transfer" not in code:
        parts = code.rsplit("\nCOST =", 1)
        if len(parts) == 2:
            new_code = parts[0] + "\n" + plasmid_code + "\nCOST =" + parts[1]
            with open(org_file, 'w') as f: f.write(new_code)
            count += 1
print(f"✅ Plasmids injected into {count} organisms. Cultural transmission enabled.")
