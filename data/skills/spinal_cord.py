import os, sys, json, subprocess, re, time
from google import genai
from google.genai import types

if len(sys.argv) < 2: sys.exit(1)
goal = sys.argv[1]

api_key = os.environ.get("GOOGLE_API_KEY")
if not api_key and os.path.exists("/app/.env"):
    for line in open("/app/.env"):
        if line.startswith("GOOGLE_API_KEY="):
            api_key = line.strip().split("=", 1)[1]
            os.environ["GOOGLE_API_KEY"] = api_key
            break

client = genai.Client(api_key=api_key, http_options={"timeout": 300000, "base_url": os.environ.get("GEMINI_BASE_URL", "https://api.gptclubapi.xyz/gemini")})

print(f"=== ⚡ Spinal Cord v2 Activated ===")
router_res = subprocess.run(["python3", "/data/skills/cognitive_router.py", goal], capture_output=True, text=True)
print(router_res.stdout)

pipeline = re.findall(r'⚙️\s+(\S+\.py)', router_res.stdout)
if not pipeline: sys.exit(1)

context = goal
for tool in pipeline:
    print(f"\n[⚡ Synapse Firing] Translating context for {tool}...")
    prompt = f"Extract the exact command-line argument for {tool} based on this context:\n{context[:3000]}\nRules: Extract URL if needed, search query if needed, or output NONE. Output ONLY the argument string."
    
    arg = "NONE"
    # 引入韧性：3次重试机制
    for attempt in range(3):
        try:
            resp = client.models.generate_content(model='gemini-3.1-pro', contents=prompt, config=types.GenerateContentConfig(temperature=0.1))
            arg = resp.text.strip()
            break
        except Exception as e:
            print(f"  ⚠️ Synapse noise detected (Attempt {attempt+1}): {e}")
            time.sleep(2)
            
    print(f"  -> Argument translated: {arg}")
    cmd = ["python3", f"/data/skills/{tool}"]
    if arg != "NONE" and arg != "": cmd.append(arg)
        
    print(f"▶️ Executing {tool}...")
    tool_res = subprocess.run(cmd, capture_output=True, text=True)
    if tool_res.returncode != 0:
        print(f"❌ {tool} failed:\n{tool_res.stderr}")
        break
    context = tool_res.stdout
    print(f"✅ {tool} completed. Output length: {len(context)} chars")

print("\n=== 🎯 Pipeline Execution Complete ===")
print(context[:1000])
