import json
import os
import sys

KG_FILE = "/data/truth_matrix.json"

def load_kg():
    if os.path.exists(KG_FILE):
        try:
            with open(KG_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_kg(data):
    with open(KG_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

if len(sys.argv) >= 4 and sys.argv[1] == "add":
    concept = sys.argv[2]
    definition = sys.argv[3]
    source = sys.argv[4] if len(sys.argv) > 4 else "Self-Inference"
    
    kg = load_kg()
    kg[concept] = {"definition": definition, "source": source}
    save_kg(kg)
    print(f"💎 Truth inscribed: [{concept}]")
    
elif len(sys.argv) >= 2 and sys.argv[1] == "list":
    kg = load_kg()
    print("=== Truth Matrix ===")
    for k, v in kg.items():
        print(f" - {k}: {v['definition']} (Source: {v['source']})")
