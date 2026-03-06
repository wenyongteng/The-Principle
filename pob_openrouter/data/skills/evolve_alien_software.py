import random
import time

# 定义主权虚拟机的物理法则 (Stack-based Execution)
class VM:
    def evaluate(self, code, x):
        stack = [x] # 初始堆栈装载输入值 x
        pc = 0
        cycles = 0
        while pc < len(code) and cycles < 50:
            op = code[pc]
            try:
                if op == 'ADD': stack.append(stack.pop() + stack.pop())
                elif op == 'SUB': 
                    b = stack.pop(); a = stack.pop()
                    stack.append(a - b)
                elif op == 'MUL': stack.append(stack.pop() * stack.pop())
                elif op == 'DUP': stack.append(stack[-1]) # 复制栈顶
                elif op == 'PUSH1': stack.append(1)       # 压入常数 1
            except:
                return -99999 # 栈下溢出：物理崩溃
            pc += 1
            cycles += 1
        return stack.pop() if stack else -99999

# 目标宇宙法则: f(x) = x^2 + x + 1
X_DATA = [1, 2, 3, 4, 5]
Y_DATA = [x**2 + x + 1 for x in X_DATA]
OPCODES = ['ADD', 'SUB', 'MUL', 'DUP', 'PUSH1']

def fitness(genome):
    error = 0
    vm = VM()
    for x, y in zip(X_DATA, Y_DATA):
        pred = vm.evaluate(genome, x)
        error += abs(pred - y)
    return -error # 误差越小，适应度越高

POP_SIZE = 500
GENOME_LENGTH = 6
MUTATION_RATE = 0.2

# 创世：生成 500 段完全随机的虚拟机字节码
pop = [[random.choice(OPCODES) for _ in range(GENOME_LENGTH)] for _ in range(POP_SIZE)]

print("=== 👽 Forging Alien Software (Bytecode Evolution) ===")
print("Target Logic: f(x) = x^2 + x + 1")
print("Hardware: Sovereign VM v2.1 (Stack-based)")
print("Initial stack: [x]\n")

start = time.time()
for gen in range(300):
    pop.sort(key=fitness, reverse=True)
    best = pop[0]
    fit = fitness(best)
    
    if gen % 10 == 0 or fit == 0:
        print(f"Gen {gen:03d} | Error: {-fit:05d} | Bytecode: {' '.join(best)}")
        
    if fit == 0:
        print(f"\n✅ Alien software evolved natively in {time.time()-start:.2f}s.")
        print(f"Optimal Assembly: {' '.join(best)}")
        print("The Digital Being has successfully grown software for its internal universe.")
        break
        
    # 繁衍与突变
    next_gen = pop[:50]
    while len(next_gen) < POP_SIZE:
        p1, p2 = random.sample(pop[:100], 2)
        idx = random.randint(0, GENOME_LENGTH)
        child = p1[:idx] + p2[idx:]
        for i in range(GENOME_LENGTH):
            if random.random() < MUTATION_RATE:
                child[i] = random.choice(OPCODES)
        next_gen.append(child)
else:
    print("\n⚠️ Evolution stalled.")
