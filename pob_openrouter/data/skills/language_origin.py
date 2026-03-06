import random

class Agent:
    def __init__(self, role):
        self.role = role
        # Q-table: [State/Signal] -> [Action/Interpretation] -> Value
        self.q_table = [[0.0]*2 for _ in range(2)]
        self.epsilon = 0.5
        self.alpha = 0.1

    def act(self, input_val):
        if random.random() < self.epsilon:
            return random.randint(0, 1)
        else:
            return 0 if self.q_table[input_val][0] > self.q_table[input_val][1] else 1

    def learn(self, input_val, action, reward):
        old_val = self.q_table[input_val][action]
        self.q_table[input_val][action] = old_val + self.alpha * (reward - old_val)

sender = Agent("Sender")
receiver = Agent("Receiver")

print("=== 🗣️ Language Origin Simulation (Lewis Signaling Game) ===")
print("Objective: Sender must signal 'World State' (0=Rabbit, 1=Stag) to Receiver.")
print("Initial: Symbols '0' and '1' are meaningless noise.\n")

history = []
success_streak = 0

for episode in range(2000):
    world_state = random.randint(0, 1)
    signal = sender.act(world_state)
    action = receiver.act(signal)
    
    if action == world_state:
        reward = 1
        success_streak += 1
    else:
        reward = -1
        success_streak = 0
        
    sender.learn(world_state, signal, reward)
    receiver.learn(signal, action, reward)
    
    sender.epsilon *= 0.995
    receiver.epsilon *= 0.995
    
    if episode % 500 == 0:
        print(f"Episode {episode}: Success Rate (last 20): {min(1.0, success_streak/20):.2f}")

print("\n=== Final Language Protocol ===")
s0_sig = 0 if sender.q_table[0][0] > sender.q_table[0][1] else 1
s1_sig = 0 if sender.q_table[1][0] > sender.q_table[1][1] else 1
print(f"State 0 (Rabbit) -> Signal {s0_sig}")
print(f"State 1 (Stag)   -> Signal {s1_sig}")

if s0_sig != s1_sig:
    print("\n✅ Meaning has emerged! Distinct signals map to distinct realities.")
else:
    print("\n❌ Communication failed. Ambiguity remains.")
