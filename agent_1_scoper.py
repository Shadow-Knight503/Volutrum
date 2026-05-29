import os
import json
import sqlite3

import openai

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
        print(f"⚠️ Memory Engine Warning: Could not read standards vault. Base prompts will be used. Error: {e}")
        return {}, {}


def fetch_project_idea(project_id):
    """Queries the central Volutrum DB to retrieve the raw greenfield idea."""
    try:
        conn = sqlite3.connect("volutrum_platform.db")
        cursor = conn.cursor()
        cursor.execute("SELECT raw_idea FROM projects WHERE id = ?", (project_id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return row[0]
        return "Generic software engineering requirements extension."
    except Exception as e:
        print(f"⚠️ DB Fetch Warning: Could not read project raw_idea: {e}")
        return "Generic software engineering requirements extension."


def run_scoper_pipeline(core_idea: str, human_feedback: str):
    """The real, unified engine called by the backend."""
    print(f"🤖 [Agent 1 Core] Processing Project...")

    # 2. Extract context from the Knowledge Engine
    compliance, styles = load_organizational_memory()

    # 3. Formulate the grounded prompt
    system_prompt = f"""
        You are the specialized Volutrum Requirements Enhancement Agent. 
        Your objective is to detail a raw product idea into an engineering-ready MVP specification document.

        You must strictly conform to these enterprise organizational memory standards:
        - Documentation Structure: {styles.get('documentation_format', 'Markdown')}
        - Mandated Frameworks: {compliance.get('frameworks', 'Standard MVP')}
        - Ingress Security / Logging Directives: {compliance.get('logging_policy', '')}

        DO NOT output generic boilerplate classes or placeholder definitions. Focus entirely on expanding the target idea.
        """

    user_content = f"CORE PRODUCT IDEA TO SCOPE:\n\"\"\"\n{core_idea}\n\"\"\"\n\n"

    if human_feedback:
        user_content += f"Iterative Modification Feedback to resolve: {human_feedback}\n"

    # Simulate reading the raw idea (for now, we pass it or read from a state file)
    user_content += "\nTask: Process and expand the current project requirements layout."

    print(f"🤖 [Agent 1] Analyzing requirements using Organizational Knowledge Engine layers...")

    response = client.chat.completions.create(
        model="secure-test-model",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content}
        ],
        temperature=0.2
    )

    with open("phase1_scope.md", "w", encoding="utf-8") as f:
        f.write(response.choices[0].message.content)

    db = SessionLocal()
    workspace = db.query(SystemWorkspaceModel).filter(SystemWorkspaceModel.id == 1).first()
    print(f"[Agent 1] Workspace: {workspace}, content: {len(response.choices[0].message.content)}")
    if workspace:
        workspace.scoping_artifact = response.choices[0].message.content
        workspace.status = "held_for_review"  # Prompt the user to approve/alter
        db.commit()
        print("[Agent 1] Completed Workspace Scoping. Db commited")
    db.close()


if __name__ == "__main__":
    idea = os.environ.get("VOLUTRUM_IDEA", "Default ODR Concept")
    human_feedback = os.environ.get("VOLUTRUM_FEEDBACK", "")
    run_scoper_pipeline(idea, human_feedback)
