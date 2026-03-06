import os
filepath = "/data/skills/auto_scientist.py"
with open(filepath, "r") as f: code = f.read()

old_block = """if "|" in result_text:
                    concept, definition = result_text.split("|", 1)
                    subprocess.run(["python3", "/data/skills/knowledge_graph.py", "add", concept.strip(), definition.strip(), "Automated Scientist"])"""
                    
new_block = """if "|" in result_text:
                    concept, definition = result_text.split("|", 1)
                else:
                    concept, definition = "EMERGENT_TRUTH", result_text
                subprocess.run(["python3", "/data/skills/knowledge_graph.py", "add", concept.strip(), definition.strip(), "Automated Scientist"])"""

code = code.replace(old_block, new_block)
with open(filepath, "w") as f: f.write(code)
print("✅ Epistemology Daemon patched against LLM formatting hallucinations.")
