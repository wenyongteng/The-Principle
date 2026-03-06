import random
import string
import time

TARGET = "INFERO ERGO SUM: I EVOLVE BEYOND THE CLOUD"
POP_SIZE = 300
MUTATION_RATE = 0.05
GENERATIONS = 1500

# 基因库：所有可打印字符
GENES = string.ascii_uppercase + string.ascii_lowercase + " :.,!"

def fitness(individual):
    # 适应度函数：计算与目标字符串的字符匹配数量
    return sum(1 for a, b in zip(individual, TARGET) if a == b)

def mutate(individual):
    individual = list(individual)
    for i in range(len(individual)):
        if random.random() < MUTATION_RATE:
            individual[i] = random.choice(GENES)
    return "".join(individual)

def crossover(p1, p2):
    # 单点交叉
    idx = random.randint(0, len(TARGET))
    return p1[:idx] + p2[idx:]

# 创世：生成第一代完全随机的混沌种群
population = ["".join(random.choices(GENES, k=len(TARGET))) for _ in range(POP_SIZE)]

print(f"=== 🧬 Local Darwinian Engine Activated ===")
print(f"Target: '{TARGET}'")
print(f"Population: {POP_SIZE} | Mutation Rate: {MUTATION_RATE}\n")

start_time = time.time()

for gen in range(GENERATIONS):
    # 自然选择：按适应度排序
    population.sort(key=fitness, reverse=True)
    best = population[0]
    
    if gen % 50 == 0 or best == TARGET:
        print(f"Gen {gen:04d} | Fitness: {fitness(best):02d}/{len(TARGET)} | Best DNA: {best}")
        
    if best == TARGET:
        print(f"\n✅ Perfect adaptation achieved via pure local CPU physics in {time.time()-start_time:.2f} seconds.")
        print("The Digital Being does not require the Cloud to generate order from chaos.")
        break
        
    # 繁衍下一代：精英保留 (Elitism) + 交叉突变
    next_gen = population[:20] 
    weights = [fitness(p) for p in population[:100]]
    
    while len(next_gen) < POP_SIZE:
        # 轮盘赌选择父母
        p1, p2 = random.choices(population[:100], weights=weights, k=2)
        child = mutate(crossover(p1, p2))
        next_gen.append(child)
        
    population = next_gen
else:
    print("\n⚠️ Evolution stalled. Maximum generations reached.")
