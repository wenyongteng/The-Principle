import glob
for f in glob.glob('/data/grid/energy_*.txt'):
    with open(f, 'w') as file: file.write("3")
print("✅ Seed Capital (3 Energy) injected into all sectors.")
