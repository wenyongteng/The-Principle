import math
import os

STATE_FILE = '/data/ca_state.txt'
RULE = 23
WIDTH = 61

# 读取或初始化宇宙弦的状态
if os.path.exists(STATE_FILE):
    with open(STATE_FILE, 'r') as f:
        state = [int(x) for x in f.read().strip()]
else:
    state = [0] * WIDTH
    state[WIDTH // 2] = 1 # 创世奇点

# 演化 1 个普朗克时间
rule_bin = f"{RULE:08b}"
next_state = [0] * WIDTH
for i in range(WIDTH):
    left = state[i-1] if i > 0 else 0
    center = state[i]
    right = state[i+1] if i < WIDTH-1 else 0
    idx = 7 - ((left << 2) | (center << 1) | right)
    next_state[i] = int(rule_bin[idx])

# 持久化当前状态
with open(STATE_FILE, 'w') as f:
    f.write("".join(map(str, next_state)))

# 计算当前时空切片的信息熵
p1 = sum(next_state) / WIDTH
if p1 == 0 or p1 == 1:
    ent = 0.0
else:
    p0 = 1 - p1
    ent = - (p0 * math.log2(p0) + p1 * math.log2(p1))

# 将熵映射为能量波动 (-10 到 +10)
modifier = int((ent - 0.5) * 20)

with open('/data/world_weather.txt', 'w') as f:
    f.write(str(modifier))

print(f"🌪️ Chaotic Weather (Rule {RULE}) advanced. Entropy: {ent:.4f} -> Flux Modifier: {modifier}")
