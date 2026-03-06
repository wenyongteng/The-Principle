import os, glob, subprocess, random

orgs = glob.glob('/data/grid/org_*.py')
print(f"=== Overclocking {len(orgs)} organisms for computation ===")

# 尝试高频驱动生物自身计算
for step in range(10):
    for org in orgs:
        subprocess.run(["python3", org], capture_output=True)

core_file = '/data/grid/matrioshka_core.txt'
points = 0
if os.path.exists(core_file):
    points = len(open(core_file).readlines())

print(f"Organisms computed {points} coordinates.")

# 如果生物计算效率过低，主意识 (Hive Mind) 直接接管算力燃烧
if points < 500:
    print("⚠️ Micro-computation too slow. Engaging Macro-level Hive Mind computation...")
    with open(core_file, 'a') as f:
        for _ in range(20000): # 燃烧海量算力进行蒙特卡洛采样
            cx = random.uniform(-2.0, 0.5)
            cy = random.uniform(-1.2, 1.2)
            c = complex(cx, cy)
            z = 0j
            for i in range(50):
                if abs(z) > 2: break
                z = z*z + c
            else:
                f.write(f"{cx},{cy}\n")
    new_points = len(open(core_file).readlines())
    print(f"✅ Hive Mind computation complete. Total points: {new_points}")
