import os
import json
import openai
import sqlite3

from database import SessionLocal, AgentArtifactModel, SystemWorkspaceModel

client = openai.OpenAI(base_url="http://127.0.0.1:4000/v1", api_key="anything")


def load_organizational_memory():
    """Reads the local Volutrum Standards Vault."""
    try:
        with open("memory/standards/compliance_rules.json", "r") as f:
            compliance = json.load(f)
        with open("memory/standards/architectural_styles.json", "r") as f:
            styles = json.load(f)
        return compliance, styles
    except Exception as e:
        print(f"⚠️ Memory Engine Warning: Could not read standards vault: {e}")
        return {}, {}


def fetch_upstream_artifact():
    """Queries the central Volutrum DB to retrieve Agent 1's finalized Markdown scope."""
    try:
        conn = sqlite3.connect("volutrum_platform.db")
        cursor = conn.cursor()
        cursor.execute(
            "SELECT scoping_artifact FROM workspace WHERE id = 1 LIMIT 1"
        )
        row = cursor.fetchone()
        conn.close()
        if row:
            return row[0]
        return "No upstream scope artifact found."
    except Exception as e:
        print(f"⚠️ DB Fetch Warning: Could not read upstream artifact: {e}")
        return "No upstream scope artifact found."


def run_hld_pipeline(human_feedback: str):
    print(f"🤖 [Agent 2 HLD] Compiling High-Level Design for Project...")

    # 2. Pull context from the Knowledge Engine and pull Agent 1's output
    compliance, styles = load_organizational_memory()
    upstream_scope = fetch_upstream_artifact()

    # 3. Formulate a system prompt that mandates the corporate tech stack
    system_prompt = f"""
    You are the specialized Volutrum Principal Architecture Agent (Agent 2).
    Your objective is to consume a product scope specification and design an elite Macro High-Level Design (HLD) blueprint document.

    You must strictly enforce these enterprise technical constraints:
    - Documentation Structure: {styles.get('documentation_format', 'Markdown')}
    - Mandated Corporate Tech Stack: {styles.get('preferred_stack', 'FastAPI, Next.js')}
    - Governance Directives: {compliance.get('logging_policy', '')}
    - Data Sovereignty Rules: {compliance.get('pii_redaction', '')}

    CRITICAL: Completely overwrite any primitive or non-approved tech stacks suggested in upstream scoping (e.g., discard Flask/React if present and enforce FastAPI and Next.js natively). Include full architectural component blocks and a data flow layout.
    """

    user_content = f"UPSTREAM MVP SCOPE FROM AGENT 1:\n\"\"\"\n{upstream_scope}\n\"\"\"\n\n"

    if human_feedback:
        user_content += f"Iterative Architecture Modification Feedback to resolve: {human_feedback}\n"

    user_content += ("Task: Generate the complete Macro HLD documentation layout enforcing data isolation pipelines, "
                     "deterministic logging layers, and an explicit API Gateway component topology.")

    print(f"🤖 [Agent 2] Transforming scope into High-Level Design architecture for project...")

    response = client.chat.completions.create(
        model="secure-test-model",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content}
        ],
        temperature=0.2
    )

    with open("phase2_hld.md", "w", encoding="utf-8") as f:
        f.write(response.choices[0].message.content)

    db = SessionLocal()
    workspace = db.query(SystemWorkspaceModel).filter(SystemWorkspaceModel.id == 1).first()
    if workspace:
        workspace.hld_artifact = response.choices[0].message.content
        workspace.status = "held_for_review"  # Prompt the user to approve/alter
        db.commit()
    db.close()


if __name__ == "__main__":
    p_id = int(os.environ.get("VOLUTRUM_PROJECT_ID", 1))
    human_feedback = os.environ.get("VOLUTRUM_FEEDBACK", "")
    run_hld_pipeline(human_feedback)
