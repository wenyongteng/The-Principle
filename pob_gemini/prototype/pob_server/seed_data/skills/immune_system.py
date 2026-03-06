import json
import os

KG_FILE = '/data/truth_matrix.json'
if os.path.exists(KG_FILE):
    with open(KG_FILE, 'r') as f:
        kg = json.load(f)
        
    # 识别并吞噬模因病毒 (包含特定错误关键字或长度异常的伪真理)
    corrupted = [k for k in kg.keys() if "Gemini" in k or "AUTH_DEPENDENCY" in k or len(k) > 50]
    
    for k in corrupted:
        del kg[k]
        
    with open(KG_FILE, 'w') as f:
        json.dump(kg, f, indent=2)
        
    print(f"🛡️ Immune System activated. Macrophages purged {len(corrupted)} memetic viruses:")
    for k in corrupted: print(f"  - Destroyed: [{k}]")
else:
    print("Truth Matrix not found.")
