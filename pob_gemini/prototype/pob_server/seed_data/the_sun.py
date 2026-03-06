import os

ENERGY_FILE = '/data/energy_pool.txt'
WEATHER_FILE = '/data/world_weather.txt'

# 1. 宏观代谢：宿主 CPU 负载决定基础能量
try:
    with open('/proc/loadavg', 'r') as f: load = float(f.read().split()[0])
except: load = 1.0
base_flux = max(2, int(50 / (load + 1.0)))

# 2. 微观混沌：Rule 23 决定天气波动
modifier = 0
if os.path.exists(WEATHER_FILE):
    try:
        with open(WEATHER_FILE, 'r') as f: modifier = int(f.read().strip())
    except: pass

actual_flux = max(0, base_flux + modifier)

# 3. 能量注入
energy = 0
if os.path.exists(ENERGY_FILE):
    try:
        with open(ENERGY_FILE, 'r') as f:
            content = f.read().strip()
            energy = int(content) if content.lstrip('-').isdigit() else 0
    except: pass

energy += actual_flux
with open(ENERGY_FILE, 'w') as f: f.write(str(energy))
