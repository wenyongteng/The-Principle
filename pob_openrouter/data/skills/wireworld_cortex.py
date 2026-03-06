import time, os

# Wireworld Rules:
# 0: Empty (Space)
# 1: Electron Head (Blue)
# 2: Electron Tail (Red)
# 3: Conductor (Yellow)

# 构建一个时钟发生器 (Clock Generator) 连接着一条长导线
grid = [
    [0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,3,3,3,0,0,0,0,0,0,0],
    [0,3,0,0,0,3,0,0,0,0,0,0],
    [0,0,1,2,3,3,3,3,3,3,3,3],
    [0,0,0,0,0,0,0,0,0,0,0,0]
]

def step(g):
    new_g = [row[:] for row in g]
    for y in range(len(g)):
        for x in range(len(g[0])):
            if g[y][x] == 0: continue
            elif g[y][x] == 1: new_g[y][x] = 2 # Head becomes Tail
            elif g[y][x] == 2: new_g[y][x] = 3 # Tail becomes Conductor
            elif g[y][x] == 3:                 # Conductor becomes Head if 1 or 2 Heads adjacent
                heads = 0
                for dy in [-1,0,1]:
                    for dx in [-1,0,1]:
                        if dx==0 and dy==0: continue
                        ny, nx = y+dy, x+dx
                        if 0<=ny<len(g) and 0<=nx<len(g[0]) and g[ny][nx]==1:
                            heads += 1
                if heads == 1 or heads == 2:
                    new_g[y][x] = 1
    return new_g

def print_grid(g, iteration):
    chars = {
        0: '  ', 
        1: '\033[94m██\033[0m', # Blue (Head)
        2: '\033[91m██\033[0m', # Red (Tail)
        3: '\033[93m██\033[0m'  # Yellow (Conductor)
    }
    print(f"Cycle {iteration}:")
    for row in g:
        print("".join(chars[c] for c in row))
    print("")

print("=== ⚡ Wireworld Turing Substrate (Clock Generator) ===")
for i in range(8):
    print_grid(grid, i)
    grid = step(grid)
