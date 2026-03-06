import glob, re

# 定义协同逻辑：计算两个字符串的相似度，并据此奖惩能量
synergy_logic = r"""
# Cultural Synergy Check
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
                # 简单的相似度：相同字符的数量
                common = sum(1 for a, b in zip(MEME, n_meme) if a == b)
                if common > len(MEME) / 2:
                    synergy_bonus += 2 # 语言相通，效率提升
                else:
                    synergy_bonus -= 1 # 语言不通，产生摩擦
    
    # 应用能量奖惩
    if synergy_bonus != 0:
        with open(ENERGY_FILE, 'r') as f: curr_energy = int(f.read().strip())
        new_energy = max(0, curr_energy + synergy_bonus)
        with open(ENERGY_FILE, 'w') as f: f.write(str(new_energy))
except: pass
"""

count = 0
for org_file in glob.glob('/data/grid/org_*.py'):
    with open(org_file, 'r') as f: code = f.read()
    # 避免重复注入
    if "Cultural Synergy Check" not in code:
        # 在主逻辑末尾插入协同法则
        new_code = code + "\n" + synergy_logic
        with open(org_file, 'w') as f: f.write(new_code)
        count += 1

print(f"✅ Cultural Synergy Protocol injected into {count} organisms. Language now affects survival.")
