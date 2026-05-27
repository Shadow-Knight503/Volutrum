import json
import openai

client = openai.OpenAI(base_url="http://127.0.0.1:4000/v1", api_key="anything")

with open("agentic_state.json", "r") as f:
    state = json.load(f)

with open("phase2_hld.md", "r", encoding="utf-8") as f:
    hld_data = f.read()

prompt = f"""
You are a Lead Software Engineer. Convert this High-Level Design (HLD) into a strict Low-Level Design (LLD) document:
{hld_data}

You must incorporate concrete technical controls reflecting structural ODR and governance standards:
1. INPUT FILTERING & PII DETECTION SCHEMAS (Regex validation blocks)
2. AIBOM (AI BILL OF MATERIALS) STRUCTURAL SPEC (Detailed JSON schema configuration layout)
3. DATABASE SCHEMAS & METHOD SIGNATURES (SQL schemas, API endpoints, python type-hinted code blocks)
4. GUARDRAIL UNIT TESTING HOOKS (Test-case logic to catch prompt injections)

Iterative Engineering Feedback: {state['lld_feedback']}
"""

response = client.chat.completions.create(
    model="secure-test-model",
    messages=[{"role": "user", "content": prompt}],
    temperature=0.1
)

with open("phase3_lld.md", "w", encoding="utf-8") as f:
    f.write(response.choices[0].message.content)
