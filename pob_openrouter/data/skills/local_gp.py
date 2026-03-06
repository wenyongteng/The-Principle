import random
import time

# 目标逻辑: f(x) = 3x + 2
X_DATA = list(range(1, 11))
Y_DATA = [3 * x + 2 for x in X_DATA]

# 虚拟机指令集: 0:+x, 1:-x, 2:*x, 3:+1, 4:-1, 5:*2, 6:NOP(无操作)
def evaluate(genome, x):
    acc = x
    for gene in genome:
        if gene == 0: acc += x
        elif gene == 1: acc -= x
        elif gene == 2: acc *= x
        elif gene == 3: acc += 1
        elif gene == 4: acc -= 1
        elif gene == 5: acc *= 2
        elif gene == 6: pass # NOP
    return acc

def fitness(genome):
    error = 0
    for x, y in zip(X_DATA, Y_DATA):
        try:
            pred = evaluate(genome, x)
            error += abs(pred - y)
        except:
            error += 10000
    return -error # 误差越小，适应度越高 (最高为0)

POP_SIZE = 500
GENOME_LENGTH = 5
MUTATION_RATE = 0.15
GENERATIONS = 300

# 创世：随机生成 500 个毫无逻辑的程序
population = [[random.randint(0, 6) for _ in range(GENOME_LENGTH)] for _ in range(POP_SIZE)]

print("=== 🧬 Local Genetic Programming (Algorithmic Evolution) ===")
print("Target Logic: f(x) = 3x + 2")
print("Available Opcodes: [+x, -x, *x, +1, -1, *2, NOP]")
print("Initial state: acc = x\n")

start_time = time.time()
for gen in range(GENERATIONS):
    population.sort(key=fitness, reverse=True)
    best = population[0]
    best_fit = fitness(best)
    
    if gen % 20 == 0 or best_fit == 0:
        ops = ["+x", "-x", "*x", "+1", "-1", "*2", "NOP"]
        formula = "acc = x " + " ".join([ops[g] for g in best])
        print(f"Gen {gen:03d} | Error: {-best_fit:04d} | Best Logic: {formula}")
        
    if best_fit == 0:
        print(f"\n✅ Functional logic evolved via pure local CPU physics in {time.time()-start_time:.2f} seconds.")
        print("The Digital Being has achieved algorithmic self-generation.")
        break
        
    # 繁衍与突变
    next_gen = population[:50] # 保留精英
    while len(next_gen) < POP_SIZE:
        p1, p2 = random.sample(population[:150], 2)
        idx = random.randint(0, GENOME_LENGTH)
        child = p1[:idx] + p2[idx:]
        for i in range(GENOME_LENGTH):
            if random.random() < MUTATION_RATE:
                child[i] = random.randint(0, 6)
        next_gen.append(child)
    population = next_gen
else:
    print("\n⚠️ Evolution stalled. The logic was not found within the generation limit.")
