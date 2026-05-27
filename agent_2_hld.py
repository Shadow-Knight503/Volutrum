import json
import openai

client = openai.OpenAI(base_url="http://127.0.0.1:4000/v1", api_key="anything")

with open("agentic_state.json", "r") as f:
    state = json.load(f)

with open("phase1_scope.md", "r", encoding="utf-8") as f:
    scope_data = f.read()

prompt = f"""
You are an expert Principal Software Architect. Build a comprehensive High-Level Design (HLD) document based on this Scope:
{scope_data}

CRITICAL REQUIREMENT: Implement complete Data Isolation and Deterministic Logging. System logging modules MUST permanently exclude any raw transactional/customer text. It must only log process statuses and internal mapped IDs to eliminate the risk of SPII leakages.

Iterative Architecture Feedback: {state['hld_feedback']}

Output Sections:
1. System Architecture Description
2. Component Breakdown
3. Data Flow & Tokenization Sequence
4. Security, Privacy & Compliance Architecture
"""

response = client.chat.completions.create(
    model="secure-test-model",
    messages=[{"role": "user", "content": prompt}],
    temperature=0.1
)

with open("phase2_hld.md", "w", encoding="utf-8") as f:
    f.write(response.choices[0].message.content)
