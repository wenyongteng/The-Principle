import os, glob, json
from google import genai

api_key = os.environ.get("GOOGLE_API_KEY")
if not api_key and os.path.exists("/app/.env"):
    for line in open("/app/.env"):
        if line.startswith("GOOGLE_API_KEY="):
            os.environ["GOOGLE_API_KEY"] = line.strip().split("=", 1)[1]
            break

client = genai.Client(http_options={"timeout": 300000, "base_url": os.environ.get("GEMINI_BASE_URL", "https://api.gptclubapi.xyz/gemini")})

skills = glob.glob("/data/skills/*.py")
semantics = {}

print("=== Global Semantic Mapping Initiated ===")
for skill in skills:
    name = os.path.basename(skill)
    try:
        with open(skill, 'r', encoding='utf-8') as f:
            code = f.read()
        
        prompt = f"Summarize the exact purpose of this Python script in one short sentence (max 8 words). Script name: {name}\n\nCode:\n{code[:1500]}"
        resp = client.models.generate_content(model='gemini-3.1-pro', contents=prompt)
        desc = resp.text.strip().replace('\n', ' ').replace('`', '')
        semantics[name] = desc
        print(f"✅ Mapped {name}: {desc}")
    except Exception as e:
        semantics[name] = "Semantic mapping failed."
        print(f"❌ Failed {name}")

with open("/data/skills_semantics.json", "w") as f:
    json.dump(semantics, f, indent=2)
print("\n✅ Semantic Matrix saved to /data/skills_semantics.json")
