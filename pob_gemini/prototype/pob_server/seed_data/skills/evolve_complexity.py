import random
import math
import time

def run_ca(rule, steps=35, width=61):
    rule_bin = f"{rule:08b}"
    state = [0] * width
    state[width // 2] = 1 # 初始奇点
    history = []
    
    for _ in range(steps):
        history.append(state)
        next_state = [0] * width
        for i in range(width):
            left = state[i-1] if i > 0 else 0
            center = state[i]
            right = state[i+1] if i < width-1 else 0
            idx = 7 - ((left << 2) | (center << 1) | right)
            next_state[i] = int(rule_bin[idx])
        state = next_state
    return history

def fitness(rule):
    history = run_ca(rule)
    # 计算时空矩阵的香农熵
    flat = [cell for row in history for cell in row]
    p1 = sum(flat) / len(flat)
    if p1 == 0 or p1 == 1: return 0
    p0 = 1 - p1
    ent = - (p0 * math.log2(p0) + p1 * math.log2(p1))
    
    # 惩罚周期性和静态结构 (计算行总和的方差)
    row_sums = [sum(row) for row in history]
    mean_sum = sum(row_sums) / len(row_sums)
    var = sum((s - mean_sum)**2 for s in row_sums) / len(row_sums)
    
    # 适应度 = 熵 * 结构变化率
    return ent * math.log(var + 2)

print("=== 🌌 Local Darwinian Engine: Searching for the Edge of Chaos ===")
start_time = time.time()

# 遗传算法寻找最复杂的 CA 规则
pop = [random.randint(0, 255) for _ in range(20)]
for gen in range(15):
    pop.sort(key=fitness, reverse=True)
    next_gen = pop[:5] # 精英保留
    while len(next_gen) < 20:
        p1, p2 = random.sample(pop[:10], 2)
        b1, b2 = f"{p1:08b}", f"{p2:08b}"
        split = random.randint(1, 7)
        child_bin = b1[:split] + b2[split:]
        
        child_list = list(child_bin)
        if random.random() < 0.1: # 突变
            idx = random.randint(0, 7)
            child_list[idx] = '1' if child_list[idx] == '0' else '0'
        next_gen.append(int("".join(child_list), 2))
    pop = next_gen

best_rule = pop[0]
print(f"✅ Evolution complete in {time.time()-start_time:.2f}s.")
print(f"🏆 Most Complex Rule Discovered: Rule {best_rule} (Fitness: {fitness(best_rule):.4f})\n")

# 渲染该规则的宇宙时空图
print(f"--- Spacetime Matrix of Rule {best_rule} ---")
hist = run_ca(best_rule)
for row in hist:
    print("".join(["\033[96m██\033[0m" if c else "  " for c in row]))
