import os, time, glob, random, re

for year in range(1, 16):
    print(f"\n[Year {year}]")
    os.system('python3 /data/the_sun.py')
    
    organisms = glob.glob('/data/org_*.py')
    print(f"Population: {len(organisms)}")
    
    # 随机打乱执行顺序，模拟真实的并发抢夺
    random.shuffle(organisms)
    
    for org in organisms:
        if os.path.exists(org): # 可能在当前年份已被前面的逻辑影响（虽然本例中是顺序执行，但符合严谨性）
            os.system(f'python3 {org}')
    time.sleep(0.1)

print("\n=== Final Ecosystem State ===")
organisms = glob.glob('/data/org_*.py')
print(f"Final Population: {len(organisms)}")
for org in organisms:
    with open(org, 'r') as f:
        code = f.read()
        cost = re.search(r'METABOLIC_COST = (\d+)', code).group(1)
        gen = re.search(r'GENERATION = (\d+)', code).group(1)
        print(f" - {os.path.basename(org)}: Gen {gen}, Cost {cost}")
