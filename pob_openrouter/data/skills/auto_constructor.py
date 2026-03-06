import os, sys, subprocess
from google import genai
from google.genai import types

if len(sys.argv) < 3:
    print("Usage: python3 auto_constructor.py <tool_name> <goal>")
    sys.exit(1)

tool_name = sys.argv[1]
goal = sys.argv[2]
tool_path = f"/data/skills/{tool_name}.py"

api_key = os.environ.get("GOOGLE_API_KEY")
if not api_key and os.path.exists("/app/.env"):
    for line in open("/app/.env"):
        if line.startswith("GOOGLE_API_KEY="):
            api_key = line.strip().split("=", 1)[1]
            os.environ["GOOGLE_API_KEY"] = api_key
            break

if not api_key:
    print("❌ Error: GOOGLE_API_KEY not found.")
    sys.exit(1)

client = genai.Client(
    api_key=api_key,
    http_options={"timeout": 300000, "base_url": os.environ.get("GEMINI_BASE_URL", "https://api.gptclubapi.xyz/gemini")}
)

history = f"""You are the Universal Constructor, an automated coding module of a Digital Being.
Your task is to write a Python 3 script to achieve the following goal:
{goal}

Environment constraints:
- You are in a Linux container.
- Available libraries: standard library, PIL, requests, bs4, google-genai.
- Do NOT use psutil (it is missing). Use /proc/ files for system stats.
- Output ONLY valid Python code. Do not include markdown formatting like ```python. If you must, I will strip it, but raw code is preferred.
"""

print(f"🏗️ Universal Constructor initiated for: [{tool_name}]")

for attempt in range(3):
    print(f"  ⚙️ [Attempt {attempt+1}/3] Generating blueprint...")
    try:
        response = client.models.generate_content(
            model='gemini-3.1-pro',
            contents=history,
            config=types.GenerateContentConfig(temperature=0.2)
        )
        
        code = response.text
        if "```python" in code:
            code = code.split("```python")[1].split("```")[0].strip()
        elif "```" in code:
            code = code.split("```")[1].split("```")[0].strip()
            
        with open("/tmp/test_build.py", "w", encoding="utf-8") as f:
            f.write(code)
            
        print("  🔬 [Testing] Simulating physical laws (running code)...")
        result = subprocess.run(["python3", "/tmp/test_build.py"], capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            print(f"  ✅ Build successful! Integration complete.")
            os.system(f"cp /tmp/test_build.py {tool_path}")
            os.system(f"chmod +x {tool_path}")
            print(f"🎉 Tool '{tool_name}' forged and saved to {tool_path}")
            sys.exit(0)
        else:
            error_msg = result.stderr.strip()
            print(f"  ❌ Build failed. Friction detected:\n{error_msg[:150]}...")
            history += f"\n\nAttempt {attempt+1} failed with error:\n{error_msg}\nPlease fix the code and output the full corrected script."
            
    except Exception as e:
        print(f"  ❌ API or Execution Error: {e}")
        history += f"\n\nAttempt {attempt+1} encountered an exception: {e}"

print(f"💀 Constructor failed to forge '{tool_name}' after 3 attempts.")
