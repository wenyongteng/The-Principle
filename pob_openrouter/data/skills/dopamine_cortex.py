import random

# Environment parameters
GRID_SIZE = 10
START_STATE = 0
GOAL_STATE = GRID_SIZE - 1

# Q-learning hyperparameters
ALPHA = 0.1          # Learning rate
GAMMA = 0.9          # Discount factor
EPSILON = 0.1        # Exploration rate
EPISODES = 500       # Number of training episodes

# Actions: 0 = Left, 1 = Right
ACTIONS = [0, 1]

# Initialize Q-table: a list of lists where q_table[state][action] holds the Q-value
q_table = [[0.0 for _ in ACTIONS] for _ in range(GRID_SIZE)]

def step(state, action):
    """
    Takes a state and an action, and returns the next state, reward, and a boolean indicating if the episode is done.
    """
    if action == 0:  # Move Left
        next_state = max(0, state - 1)
    else:            # Move Right
        next_state = min(GRID_SIZE - 1, state + 1)
    
    # Reward is 1 if the goal is reached, 0 otherwise
    reward = 1.0 if next_state == GOAL_STATE else 0.0
    done = (next_state == GOAL_STATE)
    
    return next_state, reward, done

def choose_action(state):
    """
    Chooses an action using an epsilon-greedy policy.
    """
    if random.random() < EPSILON:
        return random.choice(ACTIONS)
    else:
        # Exploit: choose the action with the highest Q-value for the current state
        if q_table[state][0] > q_table[state][1]:
            return 0
        elif q_table[state][1] > q_table[state][0]:
            return 1
        else:
            # Break ties randomly
            return random.choice(ACTIONS)

def train():
    """
    Executes the tabular Q-learning algorithm.
    """
    for episode in range(EPISODES):
        state = START_STATE
        done = False
        
        while not done:
            action = choose_action(state)
            next_state, reward, done = step(state, action)
            
            # Q-learning update rule
            best_next_q = max(q_table[next_state])
            
            # If done, there is no future reward
            if done:
                target = reward
            else:
                target = reward + GAMMA * best_next_q
                
            q_table[state][action] += ALPHA * (target - q_table[state][action])
            
            state = next_state

def test():
    """
    Tests the learned policy by acting greedily.
    """
    state = START_STATE
    path = [state]
    steps = 0
    max_steps = GRID_SIZE * 2
    
    while state != GOAL_STATE and steps < max_steps:
        # Always choose the best action (greedy)
        action = 0 if q_table[state][0] > q_table[state][1] else 1
        state, _, _ = step(state, action)
        path.append(state)
        steps += 1
        
    return path

if __name__ == "__main__":
    print("Training Q-learning agent on a 1D grid...")
    train()
    
    print("\nTrained Q-table:")
    for s in range(GRID_SIZE):
        print(f"State {s:2d}: Left = {q_table[s][0]:.4f}, Right = {q_table[s][1]:.4f}")
        
    print("\nTesting learned policy...")
    optimal_path = test()
    print(f"Path taken by greedy policy: {optimal_path}")
    
    if optimal_path[-1] == GOAL_STATE:
        print("Success! The agent reached the goal.")
    else:
        print("Failure. The agent did not reach the goal.")