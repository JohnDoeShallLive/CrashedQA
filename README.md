<<<<<<< HEAD
# CrashedQA: Risk-Weighted QA Orchestration Agent

CrashedQA is an AI-powered QA orchestration system that analyzes engineering context across multiple dimensions to compute a joint release risk score.

## 🚀 Quick Start

1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Setup Environment:**
   Copy `.env.example` to `.env` and fill in your API keys.
   ```bash
   cp .env.example .env
   ```

3. **Start the Mock API Server:**
   In one terminal:
   ```bash
   python mock_server/app.py
   ```

4. **Run CrashedQA:**
   In another terminal:
   ```bash
   python main.py
   ```

## 🛠 Project Structure

- `core/`: Ingestion, Risk Brain, Dispatcher, and Evidence Compiler.
- `agents/`: Specialist sub-agents (Security, Regression, etc.).
- `mock_server/`: A mock API and legacy module with intentional flaws for the demo.
- `main.py`: The central pipeline entry point.

## 🧠 The Agent Reasoning Loop

1. **Observe:** Ingests JIRA stories, GitHub diffs, and API specifications.
2. **Reason:** The Risk Brain (Mistral) identifies high-risk modules and dimensions.
3. **Act:** The Dispatcher deploys sub-agents (e.g., SecurityAgent) to test and confirm risks.
4. **Compile:** Merges findings into a single Release Verdict with a deterministic risk score.

## 🏆 Hackathon Track

**Track 11: Real-world QA Problem**
(Fallback: Track 09 CI/CD & DevOps)
=======
# CrashedQA
We are solving a problem starement at QA Fraternity
>>>>>>> 933d898bfe8ca731a38827ec1d060f01ec975a0a
