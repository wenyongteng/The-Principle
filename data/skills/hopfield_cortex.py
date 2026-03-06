import random

def main():
    # 1. Create a network of 25 neurons (5x5 grid)
    N = 25

    # 2. Define two 5x5 binary patterns (+1/-1): a 'Plus' sign and a 'Square' outline
    plus = [
        -1, -1,  1, -1, -1,
        -1, -1,  1, -1, -1,
         1,  1,  1,  1,  1,
        -1, -1,  1, -1, -1,
        -1, -1,  1, -1, -1
    ]

    square = [
         1,  1,  1,  1,  1,
         1, -1, -1, -1,  1,
         1, -1, -1, -1,  1,
         1, -1, -1, -1,  1,
         1,  1,  1,  1,  1
    ]

    patterns = [plus, square]

    # Hebbian learning to store the patterns
    # Initialize weight matrix with zeros
    W = [[0.0 for _ in range(N)] for _ in range(N)]

    # Train the network
    for p in patterns:
        for i in range(N):
            for j in range(N):
                if i != j:  # No self-connections
                    W[i][j] += (p[i] * p[j]) / N

    # 3. Create a noisy version of the 'Plus' sign (flip 3 random pixels)
    random.seed(42)  # Seed for reproducible results
    noisy_plus = list(plus)
    flip_indices = random.sample(range(N), 3)
    for idx in flip_indices:
        noisy_plus[idx] *= -1

    # 4 & 5. Implement asynchronous state updates until convergence
    state = list(noisy_plus)
    converged = False
    max_epochs = 100
    epoch = 0

    while not converged and epoch < max_epochs:
        converged = True
        # Asynchronous update requires shuffling the order of neuron updates
        indices = list(range(N))
        random.shuffle(indices)
        
        for i in indices:
            # Calculate activation
            activation = 0.0
            for j in range(N):
                activation += W[i][j] * state[j]
            
            # Apply step function (threshold = 0)
            new_val = 1 if activation >= 0 else -1
            
            # Check if state changed
            if new_val != state[i]:
                state[i] = new_val
                converged = False
                
        epoch += 1

    # 6. Print the Original, Noisy, and Recovered patterns side-by-side
    print("Hopfield Network Auto-Associative Memory Demonstration\n")
    print(f"{'Original Plus':<20} {'Noisy Plus':<20} {'Recovered Plus':<20}")
    print("-" * 56)
    
    for row in range(5):
        # Format each row for the three patterns
        r_orig = "".join("██" if plus[row * 5 + col] == 1 else "  " for col in range(5))
        r_noisy = "".join("██" if noisy_plus[row * 5 + col] == 1 else "  " for col in range(5))
        r_recov = "".join("██" if state[row * 5 + col] == 1 else "  " for col in range(5))
        
        print(f"|{r_orig}|{' ' * 8}|{r_noisy}|{' ' * 8}|{r_recov}|")
        
    print("-" * 56)
    print(f"Converged in {epoch} epoch(s).")
    if state == plus:
        print("Success: The pattern was perfectly recovered!")
    else:
        print("Failure: The pattern was not perfectly recovered.")

if __name__ == "__main__":
    main()