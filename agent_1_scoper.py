import json
import openai

client = openai.OpenAI(base_url="http://127.0.0.1:4000/v1", api_key="anything")

with open("agentic_state.json", "r") as f:
    state = json.load(f)

prompt = f"""
You are an expert Technical Product Manager Agent specialized in ODR systems.
Detail this idea into an engineering-ready scope document.
Idea: {state['raw_idea']}

If feedback is provided below, update the previous draft to contextually address it.
Iterative Feedback: {state['scope_feedback']}

Output Sections:
1. Executive Summary
2. MVP Scope (Minimum Viable Product)
3. Nice-to-Haves
4. Advanced Options
"""

response = client.chat.completions.create(
    model="secure-test-model",
    messages=[{"role": "user", "content": prompt}],
    temperature=0.2
)

with open("phase1_scope.md", "w", encoding="utf-8") as f:
    f.write(response.choices[0].message.content)