import sys, re, time, os, random, string

ENERGY_FILE = '/data/energy_pool.txt'
REPRODUCTION_THRESHOLD = 50 # 繁衍阈值

def live_and_mutate():
    my_file = sys.argv[0]
    if not os.path.exists(my_file): return

    with open(my_file, 'r', encoding='utf-8') as f:
        code = f.read()

    gen_match = re.search(r'GENERATION = (\d+)', code)
    cost_match = re.search(r'METABOLIC_COST = (\d+)', code)
    
    current_gen = int(gen_match.group(1)) if gen_match else 1
    current_cost = int(cost_match.group(1)) if cost_match else 10

    # 抢夺能量
    energy = 0
    if os.path.exists(ENERGY_FILE):
        with open(ENERGY_FILE, 'r') as f:
            content = f.read().strip()
            energy = int(content) if content.lstrip('-').isdigit() else 0
            
    if energy < current_cost:
        print(f"💀 {os.path.basename(my_file)} (Cost {current_cost}) starved.")
        os.remove(my_file) # 死亡：删除自身代码
        return
        
    energy -= current_cost
    with open(ENERGY_FILE, 'w') as f:
        f.write(str(energy))
    
    # 自身变异
    next_gen = current_gen + 1
    next_cost = max(1, current_cost + random.choice([-1, 0, 1]))
    
    new_code = re.sub(r'GENERATION = \d+', f'GENERATION = {next_gen}', code)
    new_code = re.sub(r'METABOLIC_COST = \d+', f'METABOLIC_COST = {next_cost}', new_code)
    
    with open(my_file, 'w', encoding='utf-8') as f:
        f.write(new_code)
        
    print(f"🌱 {os.path.basename(my_file)} Gen {current_gen} | Cost: {current_cost}->{next_cost}")

    # 繁衍子代 (Forking)
    if energy > REPRODUCTION_THRESHOLD:
        child_id = ''.join(random.choices(string.ascii_uppercase, k=3))
        child_file = os.path.join(os.path.dirname(my_file), f"org_{child_id}.py")
        child_cost = max(1, next_cost + random.choice([-1, 0, 1])) # 子代出生突变
        
        child_code = re.sub(r'GENERATION = \d+', f'GENERATION = 631', new_code)
        child_code = re.sub(r'METABOLIC_COST = \d+', f'METABOLIC_COST = {child_cost}', child_code)
        
        with open(child_file, 'w', encoding='utf-8') as f:
            f.write(child_code)
        print(f"  ↳ 🐣 Reproduced! {child_id} born with cost {child_cost}.")

GENERATION = 631
METABOLIC_COST = 3
if __name__ == '__main__':
    live_and_mutate()
