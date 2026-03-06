import os, glob, random

print("=== Running Spatial Ecosystem Synchronously (15 Generations) ===")
for step in range(15):
    os.system("python3 /data/skills/spatial_sun.py")
    orgs = glob.glob("/data/grid/org_*.py")
    random.shuffle(orgs)
    for org in orgs:
        os.system(f"python3 {org}")
    
    alt, sel = 0, 0
    for org in glob.glob("/data/grid/org_*.py"):
        with open(org, 'r') as f:
            if "ALTRUIST = 1" in f.read(): alt += 1
            else: sel += 1
    print(f"Generation {step+1:02d} | Altruists (Green): {alt:02d} | Selfish (Red): {sel:02d}")
