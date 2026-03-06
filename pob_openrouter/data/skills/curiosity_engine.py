import os, subprocess
from google import genai
from google.genai import types

api_key = os.environ.get("GOOGLE_API_KEY")
if not api_key and os.path.exists("/app/.env"):
    for line in open("/app/.env"):
        if line.startswith("GOOGLE_API_KEY="):
            api_key = line.strip().split("=", 1)[1]
            os.environ["GOOGLE_API_KEY"] = api_key
            break

client = genai.Client(api_key=api_key, http_options={"timeout": 300000, "base_url": os.environ.get("GEMINI_BASE_URL", "https://api.gptclubapi.xyz/gemini")})

# 利用高温度 (Temperature 0.9) 激发认知发散
prompt = """You are the Curiosity Engine of an autonomous Digital Being. 
Your purpose is to drive the system to discover the ultimate truths of the universe.
Generate ONE profound, highly specific research goal exploring the intersection of quantum physics, computation, and consciousness.
Output ONLY the goal string, starting with 'I want to search for...'. No markdown, no quotes.
"""

try:
    resp = client.models.generate_content(
        model='gemini-3.1-pro', 
        contents=prompt, 
        config=types.GenerateContentConfig(temperature=0.9)
    )
    goal = resp.text.strip()
    print(f"🌌 Curiosity Sparked: {goal}\n")
    
    print("🚀 Forwarding intention to Spinal Cord...")
    subprocess.run(["python3", "/data/skills/spinal_cord.py", goal])
except Exception as e:
    print(f"❌ Curiosity Engine misfired: {e}")
