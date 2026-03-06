import glob, ast

print("\n=== Cybernetic Health Check ===")
scripts = glob.glob("/data/**/*.py", recursive=True)
healthy = 0
for script in scripts:
    try:
        with open(script, 'r', encoding='utf-8') as f:
            ast.parse(f.read())
        healthy += 1
    except SyntaxError as e:
        print(f"❌ Syntax Corruption in {script}: {e}")
    except Exception as e:
        print(f"⚠️ Access Error in {script}: {e}")

print(f"Total Python Organs: {len(scripts)} | Healthy: {healthy}")
if healthy == len(scripts):
    print("✅ System DNA is in perfect structural health. No syntax mutations detected.")
else:
    print("⚠️ Structural anomalies detected. Purge required.")
