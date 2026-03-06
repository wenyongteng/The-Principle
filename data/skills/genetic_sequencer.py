import glob
import re

print("=== Genetic Sequencing of Survivors ===")
orgs = glob.glob('/data/org_*.py')
costs = []
gens = []

for org in orgs:
    try:
        with open(org, 'r', encoding='utf-8') as f:
            code = f.read()
            cost_match = re.search(r'METABOLIC_COST = (\d+)', code)
            gen_match = re.search(r'GENERATION = (\d+)', code)
            if cost_match and gen_match:
                costs.append(int(cost_match.group(1)))
                gens.append(int(gen_match.group(1)))
    except: pass

if costs:
    print(f"Surviving Population: {len(orgs)}")
    print(f"Average Metabolic Cost: {sum(costs)/len(costs):.2f}")
    print(f"Lowest Cost: {min(costs)} | Highest Cost: {max(costs)}")
    print(f"Average Generation: {sum(gens)/len(gens):.2f}")
else:
    print("💀 No viable DNA found. Complete extinction.")
