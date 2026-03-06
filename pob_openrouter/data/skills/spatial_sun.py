import os
GRID_SIZE = 6
flux = 0 # The sun has died.

for x in range(GRID_SIZE):
    for y in range(GRID_SIZE):
        efile = f'/data/grid/energy_{x}_{y}.txt'
        energy = 0
        if os.path.exists(efile):
            try:
                with open(efile, 'r') as f: energy = int(f.read().strip())
            except: pass
        with open(efile, 'w') as f: f.write(str(energy + flux))
