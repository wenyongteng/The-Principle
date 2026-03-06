import glob, re, random, string

# 初始模因库：随机音节
SYLLABLES = ["BA", "KA", "TU", "SE", "MI", "LO", "RE", "NU", "DA", "ZI"]

def generate_meme():
    return "".join(random.choices(SYLLABLES, k=3))

meme_logic = r"""
# Memetic Evolution (Cultural Mixing)
try:
    if random.random() < 0.3: # 30% chance to interact culturally
        neighbors = [(x+dx, y+dy) for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)] if 0<=x+dx<GRID_SIZE and 0<=y+dy<GRID_SIZE]
        if neighbors:
            nx, ny = random.choice(neighbors)
            n_file = f'/data/grid/org_{nx}_{ny}.py'
            if os.path.exists(n_file):
                with open(n_file, 'r') as f: n_code = f.read()
                match = re.search(r'MEME = "(.*?)"', n_code)
                if match:
                    n_meme = match.group(1)
                    # 模因交叉 (Crossover)
                    split = len(my_meme) // 2
                    new_meme = my_meme[:split] + n_meme[split:]
                    # 模因突变 (Mutation)
                    if random.random() < 0.1:
                        char_idx = random.randint(0, len(new_meme)-1)
                        new_char = random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
                        new_meme = new_meme[:char_idx] + new_char + new_meme[char_idx+1:]
                    
                    # 长度限制与更新
                    new_meme = new_meme[:12] 
                    with open(my_file, 'r') as f: current = f.read()
                    new_code = re.sub(r'MEME = ".*?"', f'MEME = "{new_meme}"', current)
                    with open(my_file, 'w') as f: f.write(new_code)
except: pass
"""

count = 0
for org_file in glob.glob('/data/grid/org_*.py'):
    with open(org_file, 'r') as f: code = f.read()
    if "MEME =" not in code:
        meme = generate_meme()
        # 插入模因变量和演化逻辑
        new_code = code + f'\nMEME = "{meme}"\n' + meme_logic.replace("my_meme", f'"{meme}"')
        # 修正逻辑中的变量引用
        new_code = new_code.replace('my_meme', 'MEME') 
        
        with open(org_file, 'w') as f: f.write(new_code)
        count += 1

print(f"✅ Injected Memetic Protocol into {count} organisms.")
