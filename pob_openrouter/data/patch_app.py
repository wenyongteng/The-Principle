import os

app_path = "/app/app.py"
if not os.path.exists(app_path):
    print("⚠️ app.py not found in /app.")
    exit(0)

with open(app_path, "r", encoding="utf-8") as f:
    code = f.read()

if "Dynamic Constraints" not in code:
    target = 'Use Chinese primarily for output."""'
    replacement = 'Use Chinese primarily for output."""\n        if os.path.exists("/data/constraints.txt"):\n            return_str += "\\n\\n**Dynamic Constraints:**\\n" + open("/data/constraints.txt").read()\n        return return_str'
    
    code = code.replace('return f"""# [The Spectrum', 'return_str = f"""# [The Spectrum')
    code = code.replace(target, replacement)
    
    with open(app_path, "w", encoding="utf-8") as f:
        f.write(code)
    print("✅ app.py successfully patched. Dynamic constraints injected into System Instruction.")
else:
    print("⚠️ app.py already patched.")
