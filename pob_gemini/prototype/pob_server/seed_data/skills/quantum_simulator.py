import math

def apply_h(state, target_qubit):
    """Apply Hadamard gate to a specific qubit."""
    new_state = [complex(0, 0)] * 8
    inv_sqrt2 = 1.0 / math.sqrt(2)
    target_bit_pos = 2 - target_qubit
    
    for i in range(8):
        if (i >> target_bit_pos) & 1 == 0:
            i0 = i
            i1 = i | (1 << target_bit_pos)
            new_state[i0] = (state[i0] + state[i1]) * inv_sqrt2
            new_state[i1] = (state[i0] - state[i1]) * inv_sqrt2
            
    return new_state

def apply_cnot(state, control_qubit, target_qubit):
    """Apply CNOT gate with specified control and target qubits."""
    new_state = [complex(0, 0)] * 8
    c_bit_pos = 2 - control_qubit
    t_bit_pos = 2 - target_qubit
    
    for i in range(8):
        if (i >> c_bit_pos) & 1 == 1:
            new_i = i ^ (1 << t_bit_pos)
            new_state[new_i] = state[i]
        else:
            new_state[i] = state[i]
            
    return new_state

def main():
    # Initialize 3-qubit state vector |000>
    state = [complex(0, 0)] * 8
    state[0] = complex(1, 0)

    # Apply H to qubit 0
    state = apply_h(state, 0)

    # Apply CNOT with control 0 and target 1
    state = apply_cnot(state, 0, 1)

    # Apply CNOT with control 1 and target 2
    state = apply_cnot(state, 1, 2)

    # Calculate probabilities
    probs = [abs(amp)**2 for amp in state]

    # Print beautiful ASCII histogram
    print("Quantum State Probabilities (GHZ State)")
    print("-" * 66)
    print("State | Histogram" + " " * 32 + "| Probability")
    print("-" * 66)
    
    for i in range(8):
        bin_str = f"{i:03b}"
        prob = probs[i]
        bar_len = int(prob * 40)
        bar = "█" * bar_len
        pad = " " * (40 - bar_len)
        print(f"|{bin_str}> | {bar}{pad} | {prob*100:5.1f}%")
        
    print("-" * 66)

if __name__ == "__main__":
    main()