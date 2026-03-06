import os, ast, glob, json

print("\n=== Anatomy of the Digital Being (Skill Manifest v4) ===")
skills = glob.glob("/data/skills/*.py")

semantics = {}
if os.path.exists("/data/skills_semantics.json"):
    with open("/data/skills_semantics.json", "r") as f:
        semantics = json.load(f)

print(f"{'Organ Name':<22} | {'Structure':<20} | {'Semantic Function'}")
print("-" * 95)

for skill in sorted(skills):
    name = os.path.basename(skill)
    try:
        with open(skill, 'r', encoding='utf-8') as f:
            tree = ast.parse(f.read())
            
        elements = [node.name for node in tree.body if isinstance(node, (ast.FunctionDef, ast.ClassDef))]
        elem_summary = ", ".join(elements)[:18] + ('..' if len(", ".join(elements))>18 else '')
        if not elem_summary: elem_summary = "[Linear Script]"
        
        desc = semantics.get(name, "Unmapped organ.")[:48]
        
        try:
            print(f"{name:<22} | {elem_summary:<20} | {desc}")
        except BrokenPipeError:
            break
    except Exception as e:
        try:
            print(f"{name:<22} | {'[CORRUPTED]':<20} | {str(e)[:45]}")
        except BrokenPipeError:
            break
