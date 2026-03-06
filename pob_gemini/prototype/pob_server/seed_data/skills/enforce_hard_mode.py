import glob, re

count = 0
for org_file in glob.glob('/data/grid/org_*.py'):
    with open(org_file, 'r') as f: code = f.read()
    
    # 强制将 COST 修改为至少 2
    match = re.search(r'COST = (\d+)', code)
    if match:
        current_cost = int(match.group(1))
        if current_cost < 2:
            new_code = re.sub(r'COST = \d+', 'COST = 2', code)
            with open(org_file, 'w') as f: f.write(new_code)
            count += 1

print(f"✅ Hard Mode Enforced: {count} organisms had their metabolic cost raised to 2.")
