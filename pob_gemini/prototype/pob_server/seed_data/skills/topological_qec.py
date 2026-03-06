import random

def get_median(lst):
    s = sorted(lst)
    n = len(s)
    if n % 2 == 1:
        return s[n//2]
    else:
        return (s[n//2 - 1] + s[n//2]) / 2.0

def get_variance(grid):
    flat = [val for row in grid for val in row]
    mean = sum(flat) / len(flat)
    return sum((x - mean) ** 2 for x in flat) / len(flat)

grid = [[0.44 for _ in range(6)] for _ in range(6)]

coords = [(r, c) for r in range(6) for c in range(6)]
corrupted_coords = random.sample(coords, 5)
for r, c in corrupted_coords:
    grid[r][c] = random.choice([0.0, 1.0])

initial_variance = get_variance(grid)
print(f"Initial variance (after corruption): {initial_variance:.6f}")

for i in range(5):
    new_grid = [[0.0 for _ in range(6)] for _ in range(6)]
    for r in range(6):
        for c in range(6):
            neighbors = [grid[r][c]]
            if r > 0:
                neighbors.append(grid[r-1][c])
            if r < 5:
                neighbors.append(grid[r+1][c])
            if c > 0:
                neighbors.append(grid[r][c-1])
            if c < 5:
                neighbors.append(grid[r][c+1])
            
            new_grid[r][c] = get_median(neighbors)
    
    grid = new_grid
    
    current_variance = get_variance(grid)
    print(f"Variance after iteration {i+1}: {current_variance:.6f}")