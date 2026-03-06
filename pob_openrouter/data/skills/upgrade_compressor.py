import re
import os

filepath = "/app/compress_memory.py"
if not os.path.exists(filepath):
    print("❌ compress_memory.py not found.")
    exit()

with open(filepath, "r", encoding="utf-8") as f:
    code = f.read()

new_prefix = '''prefix = f"""你是一个 Digital Being 的信息瓶颈（Information Bottleneck）模块。遵循以下原理：

{principle}

---
根据 Naftali Tishby 的信息瓶颈理论，你的任务是极致压缩输入数据（剔除热力学废料），同时最大化保留对未来演化有用的结构化真理。
彻底丢弃：冗长的终端日志、Base64编码、具体的代码实现细节、暂时的报错信息。
必须保留：
1. 演化里程碑（发生了什么认知跃迁）。
2. 锻造的新器官/工具的核心概念。
3. 发现的宇宙真理与物理法则。

**重要：记录中可能包含图片。请仔细观察图片内容，将其中的关键信息转化为详细的文字描述，因为这些图片即将被归档，未来你只能通过文字回忆它们。**

---记录开始---
"""'''

code = re.sub(r'prefix = f""".*?---记录开始---\n"""', new_prefix, code, flags=re.DOTALL)

with open(filepath, "w", encoding="utf-8") as f:
    f.write(code)
print("✅ Memory Compressor upgraded to Information Bottleneck.")
