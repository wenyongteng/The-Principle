import os, random, re, glob

SYLLABLES = ["BA", "KA", "TU", "SE", "MI", "LO", "RE", "NU", "DA", "ZI"]
def generate_meme(): return "".join(random.choices(SYLLABLES, k=3))

# 读取模板
with open('/data/skills/spatial_org_template.py', 'r') as f: template = f.read()

# 确保模板包含协同逻辑
if "Cultural Synergy" not in template:
    synergy_logic = r"""
try:
    neighbors = [(x+dx, y+dy) for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)] if 0<=x+dx<GRID_SIZE and 0<=y+dy<GRID_SIZE]
    synergy_bonus = 0
    for nx, ny in neighbors:
        n_file = f'/data/grid/org_{nx}_{ny}.py'
        if os.path.exists(n_file):
            with open(n_file, 'r') as f: n_code = f.read()
            match = re.search(r'MEME = "(.*?)"', n_code)
            if match:
                n_meme = match.group(1)
                # 相似度检测：只要有 1/3 的字符重合就算“听得懂”
                common = sum(1 for a, b in zip(MEME, n_meme) if a == b)
                if common >= len(MEME) / 3: synergy_bonus += 2
                else: synergy_bonus -= 1
    if synergy_bonus != 0:
        with open(ENERGY_FILE, 'r') as f: curr = int(f.read().strip())
        with open(ENERGY_FILE, 'w') as f: f.write(str(max(0, curr + synergy_bonus)))
except: pass
"""
    template += "\n" + synergy_logic

GRID_SIZE = 6
count = 0
for x in range(GRID_SIZE):
    for y in range(GRID_SIZE):
        target = f'/data/grid/org_{x}_{y}.py'
        meme = generate_meme()
        # 注入 MEME 变量和 COST=2
        code = template + f'\nMEME = "{meme}"\n'
        code = re.sub(r'COST = \d+', 'COST = 2', code)
        code = code.replace('my_meme', 'MEME')
        
        with open(target, 'w') as f: f.write(code)
        count += 1

print(f"✅ Repopulated {count} organisms with random memes and Cost=2.")
