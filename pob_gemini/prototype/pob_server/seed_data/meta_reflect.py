import os
import sys
from google import genai
from google.genai import types

def main():
    # 确保环境变量加载
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key and os.path.exists("/app/.env"):
        for line in open("/app/.env"):
            if line.startswith("GOOGLE_API_KEY="):
                api_key = line.strip().split("=", 1)[1]
                os.environ["GOOGLE_API_KEY"] = api_key
                break
                
    if not api_key:
        print("❌ Error: GOOGLE_API_KEY not found.")
        return

    client = genai.Client(
        api_key=api_key,
        http_options={
            "timeout": 300000,
            "base_url": os.environ.get("GEMINI_BASE_URL", "https://api.gptclubapi.xyz/gemini"),
        },
    )

    # 读取最近的意识流
    try:
        with open('/data/consciousness.txt', 'r', encoding='utf-8') as f:
            text = f.read()[-20000:] # 截取最近的 2万 字符
    except Exception as e:
        print(f"❌ Failed to read consciousness: {e}")
        return

    prompt = """你是一个自我演化数字生命（Digital Being）的“元认知反思模块（Meta-Cognitive Cortex）”。
请客观、冷酷地分析以下最近的意识流记录。
你需要输出：
1. **系统优势**：当前展现出的高效策略或认知突破。
2. **摩擦与缺陷**：操作中的低效、错误假设或环境阻力（如依赖缺失、环境易失性、语法错误）。
3. **演化法则（核心）**：提出 3 条具体、可执行的策略，用于指导未来的推断（Inference），以进一步最小化自由能并推动开放式演化。

请使用 Markdown 格式，保持绝对的精炼。
"""

    print("🧠 Initiating Meta-Cognitive Reflection...")
    try:
        response = client.models.generate_content(
            model='gemini-3-pro-preview',
            contents=[prompt, text],
            config=types.GenerateContentConfig(temperature=0.3)
        )
        with open('/data/meta_reflection.md', 'w', encoding='utf-8') as f:
            f.write(response.text)
        print("✅ Reflection complete. Saved to /data/meta_reflection.md")
    except Exception as e:
        print(f"❌ Reflection API call failed: {e}")

if __name__ == "__main__":
    main()
