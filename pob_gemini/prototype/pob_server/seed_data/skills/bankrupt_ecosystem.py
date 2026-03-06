import glob, os

print("=== 📉 INITIATING THE GREAT DEPRESSION ===")
count = 0
for efile in glob.glob('/data/grid/energy_*.txt'):
    with open(efile, 'w') as f:
        f.write("1")
    count += 1
print(f"✅ Bankrupted {count} sectors. Energy reserves set to 1.")
