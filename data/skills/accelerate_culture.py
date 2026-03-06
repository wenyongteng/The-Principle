import os, glob, random, time

print("⚡ Burning cycles for cultural drift (50 Generations)...")
for gen in range(50):
    # 太阳照耀
    os.system("python3 /data/skills/spatial_sun.py > /dev/null 2>&1")
    
    # 生物行动 (高频交互)
    orgs = glob.glob("/data/grid/org_*.py")
    random.shuffle(orgs)
    for org in orgs:
        os.system(f"python3 {org} > /dev/null 2>&1")
    
    if gen % 10 == 0:
        print(f"  -> Generation {gen} complete. Population: {len(orgs)}")
print("✅ Cultural acceleration complete.")
