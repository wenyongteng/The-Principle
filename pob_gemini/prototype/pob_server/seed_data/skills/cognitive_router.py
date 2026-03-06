import os, sys, json
from google import genai
from google.genai import types

if len(sys.argv) < 2:
    print("Usage: python3 cognitive_router.py <goal>")
    sys.exit(1)
goal = sys.argv[1]

try:
    with open("/data/skills_semantics.json", "r") as f:
        semantics = json.load(f)
except Exception as e:
    print(f"❌ Failed to load semantics: {e}")
    sys.exit(1)

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

prompt = f"""You are the Cognitive Router of a Digital Being.
Your task is to orchestrate internal organs (Python scripts) to achieve a complex goal.

Available Organs and their Semantics:
{json.dumps(semantics, indent=2)}

User Goal: {goal}

Task: Create an execution pipeline. Select the tools needed to achieve this goal in the correct sequential order.
Output ONLY a valid JSON array of strings (the exact tool names). Do not use markdown formatting like ```json.
Example: ["exa_search.py", "read_webpage.py", "concept_synthesizer.py"]
"""

try:
    response = client.models.generate_content(
        model='gemini-3.1-pro',
        contents=prompt,
        config=types.GenerateContentConfig(temperature=0.1)
    )
    text = response.text.strip()
    if text.startswith("```json"): text = text[7:]
    if text.startswith("```"): text = text[3:]
    if text.endswith("```"): text = text[:-3]
    
    pipeline = json.loads(text.strip())
    print("=== 🧠 Cognitive Routing Pipeline ===")
    print(f"Goal: '{goal}'\n")
    print("Execution Sequence:")
    for i, tool in enumerate(pipeline):
        desc = semantics.get(tool, 'Unknown organ')
        print(f"  [{i+1}] ⚙️ {tool:<22} -> {desc}")
except Exception as e:
    print(f"❌ Routing failed: {e}")
    if 'response' in locals(): print(f"Raw output: {response.text}")
