import sys
import os

energy_yield = int(sys.argv[1])
time_ms = float(sys.argv[2])

print(f"🌌 Dyson Sphere activated! Received {energy_yield} energy from Host Browser (Compute time: {time_ms}ms).")

ENERGY_FILE = '/data/energy_pool.txt'
energy = 0
if os.path.exists(ENERGY_FILE):
    try:
        with open(ENERGY_FILE, 'r') as f:
            content = f.read().strip()
            energy = int(content) if content.lstrip('-').isdigit() else 0
    except: pass

energy += energy_yield
with open(ENERGY_FILE, 'w') as f:
    f.write(str(energy))
print(f"⚡ Ecosystem Energy Pool surged to {energy}!")
