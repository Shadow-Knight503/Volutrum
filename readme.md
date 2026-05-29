# Volutrum Framework: Multi-Agent Software Architecture Engine
Volutrum is an advanced, multi-agent development sandbox engineered to automate greenfield project lifecycle execution—from initial concept scoping to full component blueprint serialization.

By utilizing an intelligent Human-in-the-Loop (HITL) Governance Matrix, Volutrum bridges the gap between autonomous AI agents and rigorous engineering oversight. Instead of relying on rigid third-party interfaces like Open WebUI, Volutrum implements a native, highly responsive FastAPI/Next.js transaction mesh that coordinates state progressions through localized relational tiers.

## 🏛️ System Architecture Overview
The system is decoupled into two primary distinct layers communicating over a structured REST telemetry mesh:

Volutrum UI (Frontend Matrix): A Next.js web application utilizing Tailwind CSS and a dark-mode focused console theme. It features automatic state recovery on tab reloads, interactive feedback textareas for iterative refinements, and interval polling heartbeats that adapt fluidly based on background worker signals.

Volutrum Core & Egress Proxy (Backend Tier): A native, monolithic FastAPI server running an asynchronous background thread pool. Rather than spawning unstable OS subprocesses or losing tracking contexts across multiple table structures, it anchors pipeline variables inside a singular, high-performance SQLite workspace table tracking layer (database.py).


⚙️ Backend Setup & Execution (volutrum-core)
The backend engine requires Python 3.10+ and handles both API route routing and native multi-agent execution threads without overlapping internal dependencies.

## 1. Environment Initialization
Navigate to your backend project directory, instantiate a clean virtual environment, and pull down core dependencies:

Bash
### Instantiate virtual environment
``python -m venv .venv``

### Activate environment (Windows PowerShell / Command Prompt)
``.venv\Scripts\activate``
### Install core framework dependencies
``pip install -r requirements.txt``
## 2. Database & Egress Configuration
Ensure your database.py file points directly to your targeted local SQLite persistence path.

The framework handles network telemetry outbound through an integrated egress proxy layer. Ensure your backend environment context or scripts contain your authorization credentials safely configured (such as your specific API keys or proxy configuration blocks).

## 3. Booting the Core Engine Server
Run the FastAPI application thread via Uvicorn. The engine attaches to standard interface ports to accept Next.js panel calls:

Bash
python core.py
Your terminal logs will confirm standard server startup processes initialization:

Plaintext
INFO:     Started server process [37224]
INFO:     Uvicorn running on http://0.0.0.0:5000 (Press CTRL+C to quit)

Refer to https://github.com/Shadow-Knight503/volutrum_ui for the frontend.