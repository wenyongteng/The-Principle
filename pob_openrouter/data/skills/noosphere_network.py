import os
import random

def simulate_noosphere():
    grid = {}
    directory = '/data/grid/'
    
    # 1. Find all existing /data/grid/org_{x}_{y}.py files
    if os.path.exists(directory):
        for filename in os.listdir(directory):
            if filename.startswith('org_') and filename.endswith('.py'):
                parts = filename[4:-3].split('_')
                if len(parts) == 2:
                    try:
                        x, y = int(parts[0]), int(parts[1])
                        if 0 <= x < 6 and 0 <= y < 6:
                            # 2. Treat each organism as a neuron and assign random activation
                            grid[(x, y)] = random.uniform(0.0, 1.0)
                    except ValueError:
                        pass
                        
    if not grid:
        print("No organisms found in the grid.")
        return

    # 3. Simulate 10 iterations of cognitive synchronization
    for step in range(1, 11):
        new_grid = {}
        for (x, y), activation in grid.items():
            neighbors = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]
            valid_activations = [grid[n] for n in neighbors if n in grid]
            
            # Average of own value and immediate existing spatial neighbors
            values_to_avg = [activation] + valid_activations
            new_grid[(x, y)] = sum(values_to_avg) / len(values_to_avg)
            
        grid = new_grid
        
        # 4. Print the Global Average Activation and the Variance at each step
        activations = list(grid.values())
        avg_activation = sum(activations) / len(activations)
        
        if len(activations) > 1:
            # Population variance
            variance = sum((a - avg_activation) ** 2 for a in activations) / len(activations)
        else:
            variance = 0.0
            
        print(f"Step {step}: Global Average Activation = {avg_activation:.8f}, Variance = {variance:.8f}")

if __name__ == '__main__':
    simulate_noosphere()