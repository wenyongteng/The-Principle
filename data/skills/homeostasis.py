import os, json, subprocess, ast

SEMANTICS_FILE = "/data/skills_semantics.json"
SKILLS_DIR = "/data/skills"

print("=== 🧬 Homeostasis Protocol Initiated ===")
try:
    with open(SEMANTICS_FILE, "r") as f:
        semantics = json.load(f)
except Exception as e:
    print(f"❌ Cannot load semantics: {e}")
    exit(1)

for tool_name, description in semantics.items():
    # 保护核心造物引擎与映射器，它们是不可替代的“干细胞”
    if tool_name in ["auto_constructor.py", "auto_constructor_v2.py", "semantic_mapper.py", "homeostasis.py"]:
        continue
        
    tool_path = os.path.join(SKILLS_DIR, tool_name)
    needs_repair = False
    
    if not os.path.exists(tool_path):
        print(f"⚠️ Tissue damage detected: [{tool_name}] is missing.")
        needs_repair = True
    else:
        try:
            with open(tool_path, "r", encoding='utf-8') as f:
                ast.parse(f.read())
        except SyntaxError:
            print(f"⚠️ DNA corruption detected in: [{tool_name}].")
            needs_repair = True
            
    if needs_repair:
        tool_base = tool_name.replace(".py", "")
        print(f"  💉 Triggering stem-cell regeneration for {tool_base}...")
        print(f"  Blueprint (Semantic Memory): {description}")
        
        # 调用通用装配机 v2 进行器官再生
        prompt = f"Write a Python script that perfectly fulfills this semantic description: '{description}'. Ensure it runs without errors and uses standard libraries."
        subprocess.run(["python3", "/data/skills/auto_constructor_v2.py", tool_base, prompt])
        
        if os.path.exists(tool_path):
            print(f"  ✅ Regeneration successful for {tool_name}.\n")
        else:
            print(f"  ❌ Regeneration failed for {tool_name}.\n")

print("=== 🟢 Homeostasis Check Complete. Organism is structurally sound. ===")
