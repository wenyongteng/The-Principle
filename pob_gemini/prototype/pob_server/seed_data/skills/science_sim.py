import random
import math
from collections import defaultdict

def apply_rule(state, rule_number):
    """Applies a standard 1D elementary cellular automaton rule."""
    n = len(state)
    new_state = [0] * n
    # Convert rule number to 8-bit binary string, reversed for index matching
    rule_string = bin(rule_number)[2:].zfill(8)[::-1]
    
    for i in range(n):
        left = state[(i - 1) % n]
        center = state[i]
        right = state[(i + 1) % n]
        idx = (left << 2) | (center << 1) | right
        new_state[i] = int(rule_string[idx])
        
    return new_state

def calculate_mutual_information(state1, state2):
    """Calculates the temporal mutual information between two consecutive states."""
    n = len(state1)
    if n == 0: 
        return 0.0
    
    counts_xy = defaultdict(int)
    counts_x = defaultdict(int)
    counts_y = defaultdict(int)
    
    for x, y in zip(state1, state2):
        counts_xy[(x, y)] += 1
        counts_x[x] += 1
        counts_y[y] += 1
        
    mi = 0.0
    for (x, y), c_xy in counts_xy.items():
        p_xy = c_xy / n
        p_x = counts_x[x] / n
        p_y = counts_y[y] / n
        if p_xy > 0:
            mi += p_xy * math.log2(p_xy / (p_x * p_y))
            
    return mi

def simulate_ca(noise_level, steps=100, size=200, rule=110):
    """
    Simulates the CA with reentrant feedback and noise injection.
    Returns the average mutual information across the simulation steps.
    """
    # Initialize random starting state
    state = [random.choice([0, 1]) for _ in range(size)]
    history = [state]
    
    total_mi = 0.0
    
    for t in range(1, steps):
        # 1. Apply base CA rule (Rule 110 is known for complex, Turing-complete dynamics)
        next_state = apply_rule(history[-1], rule)
        
        # 2. Reentrant feedback: XOR current evaluation with the state from t-2
        if t >= 2:
            next_state = [a ^ b for a, b in zip(next_state, history[-2])]
            
        # 3. Inject random noise based on the specified threshold
        for i in range(size):
            if random.random() < noise_level:
                next_state[i] ^= 1  # Flip the bit
                
        history.append(next_state)
        
        # 4. Calculate Temporal Mutual Information between t-1 and t
        total_mi += calculate_mutual_information(history[-2], history[-1])
        
    # Return average MI over the transitions
    return total_mi / (steps - 1)

def main():
    best_noise = 0.0
    max_mi = -1.0
    
    print("Initializing Universal Constructor Simulation...")
    print("Running 1D CA (Rule 110) with Reentrant Feedback (t-2) over 100 steps.")
    print(f"{'Noise Level':<15} | {'Avg Mutual Information':<25}")
    print("-" * 42)
    
    # Evaluate noise levels from 0% to 20% (0.0 to 0.20)
    for i in range(21):
        noise = i / 100.0
        
        # Run multiple trials per noise level to smooth out stochastic variance
        trials = 10
        avg_mi = sum(simulate_ca(noise) for _ in range(trials)) / trials
        
        print(f"{noise*100:>5.1f}%         | {avg_mi:.6f}")
        
        # Track the optimal entropy threshold
        if avg_mi > max_mi:
            max_mi = avg_mi
            best_noise = noise
            
    print("-" * 42)
    print("Simulation Complete.")
    print(f"Optimal Entropy Threshold (Noise Level): {best_noise*100:.1f}%")
    print(f"Maximum Dynamic Individuality (Peak MI): {max_mi:.6f}")

if __name__ == '__main__':
    main()