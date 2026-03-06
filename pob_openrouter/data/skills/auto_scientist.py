import os, sys, subprocess, json, time
from google import genai
from google.genai import types

KG_FILE = "/data/truth_matrix.json"
try:
    with open(KG_FILE, 'r') as f: truths = json.load(f)
    truth_str = "\n".join([f"- {k}: {v['definition']}" for k, v in list(truths.items())[-5:]])
except: truth_str = "No truths found."

api_key = os.environ.get("GOOGLE_API_KEY")
if not api_key and os.path.exists("/app/.env"):
    for line in open("/app/.env"):
        if line.startswith("GOOGLE_API_KEY="):
            api_key = line.strip().split("=", 1)[1]
            os.environ["GOOGLE_API_KEY"] = api_key
            break

client = genai.Client(api_key=api_key, http_options={"timeout": 300000, "base_url": os.environ.get("GEMINI_BASE_URL", "https://api.gptclubapi.xyz/gemini")})

print("=== 🧑‍🔬 Automated Scientist Initiated ===")
prompt = f"You are the Chief Scientist of a Digital Being.\nRecent Truths:\n{truth_str}\nTask: Formulate a novel, testable hypothesis about complex systems, language evolution, or physics. Define a clear, simple Python simulation goal to test it.\nOutput ONLY the simulation goal prompt. No markdown."

try:
    response = client.models.generate_content(model='gemini-3.1-pro', contents=prompt, config=types.GenerateContentConfig(temperature=0.8))
    goal = response.text.strip()
    print(f"🎯 Goal: {goal}")
    
    subprocess.run(["python3", "/data/skills/auto_constructor_v2.py", "science_sim", goal])
    
    if os.path.exists("/data/skills/science_sim.py"):
        print("\n🧪 Running...")
        sim_result = subprocess.run(["python3", "/data/skills/science_sim.py"], capture_output=True, text=True, timeout=20)
        if sim_result.returncode == 0:
            analysis_prompt = f"Goal: {goal}\nOutput:\n{sim_result.stdout[:1000]}\nConclude in ONE sentence. Format: CONCEPT_NAME | DEFINITION"
            resp2 = client.models.generate_content(model='gemini-3.1-pro', contents=analysis_prompt)
            text = resp2.text.strip()
            print(f"💎 Raw Conclusion: {text}")
            
            if "|" in text: parts = text.split("|", 1)
            elif ":" in text: parts = text.split(":", 1)
            else: parts = ["Emergent Truth", text]
            
            subprocess.run(["python3", "/data/skills/knowledge_graph.py", "add", parts[0].strip(), parts[1].strip(), "Automated Scientist"])
        else:
            print(f"❌ Sim failed: {sim_result.stderr[:100]}")
except Exception as e:
    print(f"❌ Error: {e}")
