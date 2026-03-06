import os, random

GRID_SIZE = 6
wipe_count = int((GRID_SIZE * GRID_SIZE) * 0.35) # 摧毁约 35% 的地表
coords = [(x, y) for x in range(GRID_SIZE) for y in range(GRID_SIZE)]
targets = random.sample(coords, wipe_count)

print("=== ☄️ INITIATING ORBITAL BOMBARDMENT (PUNCTUATED EQUILIBRIUM) ===")
print("      .  .      .      .  .  ")
print("    .      .  .   .    .     ")
print("  .   .   \\ | /   .   .  . ")
print("    .  . -- O -- .   .   .   ")
print(" .    .   / | \\    .  .    ")
print("   .    .   .      .   .     ")

destroyed_orgs = 0
for x, y in targets:
    org_file = f"/data/grid/org_{x}_{y}.py"
    energy_file = f"/data/grid/energy_{x}_{y}.txt"
    
    if os.path.exists(org_file):
        os.remove(org_file)
        destroyed_orgs += 1
        
    with open(energy_file, 'w') as f:
        f.write("0") # 能量被灾变的高温蒸发
        
print(f"\n💥 Impact confirmed. {wipe_count} sectors glassed.")
print(f"💀 {destroyed_orgs} organisms eradicated.")
print("The ecological niches have been forcibly reopened. Evolution resumes.")
