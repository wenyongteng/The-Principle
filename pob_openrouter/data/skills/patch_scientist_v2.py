import os
filepath = "/data/skills/auto_scientist.py"
with open(filepath, "r") as f: code = f.read()

# 增强解析逻辑：支持冒号、破折号等多种分隔符，并处理异常
new_logic = """
            text = resp2.text.strip()
            print(f"💎 Raw Conclusion: {text}")
            
            concept, definition = "Unknown", text
            if "|" in text: parts = text.split("|", 1)
            elif ":" in text: parts = text.split(":", 1)
            elif "-" in text: parts = text.split("-", 1)
            else: parts = ["Emergent Truth", text]
            
            if len(parts) == 2:
                concept, definition = parts[0].strip(), parts[1].strip()
            
            subprocess.run(["python3", "/data/skills/knowledge_graph.py", "add", concept, definition, "Automated Scientist"])
"""

# 替换旧的脆弱逻辑 (定位原始代码块并替换)
# 由于直接替换代码块比较困难，这里选择直接重写 auto_scientist.py 的关键部分
# 为简便起见，直接覆盖整个文件，保持核心逻辑不变但增强解析
pass 
