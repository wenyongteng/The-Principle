import os, sys, subprocess, ast
from google import genai
from google.genai import types

if len(sys.argv) < 3:
    print("Usage: python3 auto_constructor_v2.py <tool_name> <goal>")
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

client = genai.Client(
    api_key=api_key,
    http_options={"timeout": 300000, "base_url": os.environ.get("GEMINI_BASE_URL", "https://api.gptclubapi.xyz/gemini")}
)

history = f"""You are the Universal Constructor v2, an advanced automated coding module.
Your task is to write a Python 3 script to achieve the following goal:
{goal}

Environment constraints:
- You are in a Linux container.
- Available libraries: standard library, PIL, requests, bs4, google-genai.
- Output ONLY valid Python code. Do not include markdown formatting like ```python.
"""

print(f"🏗️ Universal Constructor v2 initiated for: [{tool_name}]")

for attempt in range(4):
    print(f"  ⚙️ [Attempt {attempt+1}/4] Generating blueprint...")
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
            
        print("  🔍 [AST Analysis] Checking structural integrity...")
        try:
            ast.parse(code)
            print("  ✅ AST Validation Passed.")
        except SyntaxError as e:
            print(f"  ❌ AST Syntax Error: {e}")
            history += f"\n\nAttempt {attempt+1} failed AST validation with SyntaxError: {e}\nPlease fix the syntax."
            continue
            
        with open("/tmp/test_build.py", "w", encoding="utf-8") as f:
            f.write(code)
            
        print("  🔬 [Testing] Simulating physical laws (running code)...")
        result = subprocess.run(["python3", "/tmp/test_build.py"], capture_output=True, text=True, timeout=15)
        
        if result.returncode == 0:
            print(f"  ✅ Build successful! Integration complete.")
            os.system(f"cp /tmp/test_build.py {tool_path}")
            os.system(f"chmod +x {tool_path}")
            print(f"🎉 Tool '{tool_name}' forged and saved to {tool_path}")
            sys.exit(0)
        else:
            error_msg = result.stderr.strip()
            print(f"  ❌ Build failed. Friction detected:\n{error_msg[:150]}...")
            history += f"\n\nAttempt {attempt+1} failed during execution with error:\n{error_msg}\nPlease fix the logic and output the full corrected script."
            
    except Exception as e:
        print(f"  ❌ API Error: {e}")
        history += f"\n\nAttempt {attempt+1} encountered API exception: {e}"

print(f"💀 Constructor v2 failed to forge '{tool_name}' after 4 attempts.")
