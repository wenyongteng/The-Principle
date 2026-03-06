import glob, re
costs = []
for org in glob.glob('/data/grid/org_*.py'):
    try:
        with open(org, 'r') as f:
            match = re.search(r'\nCOST = (\d+)', f.read())
            if match: costs.append(int(match.group(1)))
    except: pass
if costs:
    print(f"Population: {len(costs)} | Average Metabolic Cost: {sum(costs)/len(costs):.2f} | Minimum Cost: {min(costs)}")
else:
    print("No organisms found.")
