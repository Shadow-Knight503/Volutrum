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
    """Queries the central Volutrum DB to retrieve Agent 2's finalized HLD architecture."""
    try:
        conn = sqlite3.connect("volutrum_platform.db")
        cursor = conn.cursor()
        cursor.execute(
            "SELECT hld_artifact FROM workspace WHERE id = 1 LIMIT 1"
        )
        row = cursor.fetchone()
        conn.close()
        if row:
            return row[0]
        return "No upstream HLD artifact found."
    except Exception as e:
        print(f"⚠️ DB Fetch Warning: Could not read upstream artifact: {e}")
        return "No upstream HLD artifact found."


def run_lld_pipeline(human_feedback: str):
    print(f"🤖 [Agent 3 LLD] Compiling Low-Level Design for Project...")

    # 2. Extract organizational context and ingest Agent 2's HLD
    compliance, styles = load_organizational_memory()
    upstream_hld = fetch_upstream_artifact()

    # 3. Formulate the low-level technical engineering prompt
    system_prompt = f"""
    You are the specialized Volutrum Low-Level Design (LLD) Patch Engineer (Agent 3).
    Your objective is to take a Macro High-Level Design (HLD) and output a highly granular, execution-ready Low-Level Design documentation pack.

    You must strictly conform to these enterprise operational requirements:
    - Documentation Style: {styles.get('documentation_format', 'Markdown with type-hinted code blocks')}
    - Mandated Codebase Architecture: {styles.get('preferred_stack', 'FastAPI, Next.js')}
    - Non-Functional Verification: {styles.get('verification_metrics', '')}

    CRITICAL: You must generate a highly granular, structured layout specifying exact API endpoints, precise request/response schemas, regex data sanitization layers, PyTest test definitions, and an explicit JSON schema template configuration block for the system's AI Bill of Materials (AIBOM).
    """

    user_content = f"UPSTREAM ARCHITECTURE SPEC FROM AGENT 2:\n\"\"\"\n{upstream_hld}\n\"\"\"\n\n"

    if human_feedback:
        user_content += f"Iterative LLD Modification Feedback to resolve: {human_feedback}\n"

    user_content += "Task: Generate the comprehensive execution-ready LLD pack, including database migration fields, input validation parameters, and the structural verification AIBOM configuration."

    print(f"🤖 [Agent 3] Compiling low-level blueprint and tracking metrics for project...")

    response = client.chat.completions.create(
        model="secure-test-model",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content}
        ],
        temperature=0.2
    )

    with open("phase3_lld.md", "w", encoding="utf-8") as f:
        f.write(response.choices[0].message.content)

    db = SessionLocal()
    workspace = db.query(SystemWorkspaceModel).filter(SystemWorkspaceModel.id == 1).first()
    if workspace:
        workspace.lld_artifact = response.choices[0].message.content
        workspace.status = "held_for_review"  # Prompt the user to approve/alter
        db.commit()
    db.close()


if __name__ == "__main__":
    p_id = int(os.environ.get("VOLUTRUM_PROJECT_ID", 1))
    human_feedback = os.environ.get("VOLUTRUM_FEEDBACK", "")
    run_lld_pipeline(human_feedback)
