# Sentinel - Agent of Agents

Observe. Audit. Trust. Optimize.

Sentinel is an enterprise AgentOps Control Tower that observes, audits, governs and optimizes AI agents. It is packaged as a single Streamlit application for Streamlit Community Cloud while preserving clean internal boundaries across services, repositories, agents, models and frontend components.

## Run Locally

```bash
python3 -m pip install -r requirements.txt
streamlit run app.py
```

The application automatically initializes SQLite and seeds permanent Demo Mode data on startup.

## Demo Walkthrough

Recommended executive demo order:

1. Dashboard: Open with enterprise health, risks and latest Sentinel signals.
2. Agent Catalogue: Show the governed inventory of enterprise AI agents.
3. Agent Details: Drill into ownership, Trust Score and audit history.
4. Live Agent Audit: Run Sentinel as an Agent-of-Agents Auditor.
5. Analytics: Close with trust, policy, cost and recommendation trends.

## Demo Mode

Demo Mode is permanent and includes three predefined enterprise scenarios:

- HR Assistant: PII leak -> Policy FAIL
- Finance Copilot: Hallucination detected
- Procurement Agent: High token usage -> Cost Optimization

## Streamlit Community Cloud Deployment

Use these settings:

- Repository: this project repository
- Branch: your deployment branch
- Main file path: `app.py`
- Python dependencies: `requirements.txt`
- Streamlit configuration: `.streamlit/config.toml`

No separate FastAPI server is required for the deployed demo.

## Deployment Checklist

- Confirm the app starts locally with `streamlit run app.py`.
- Confirm Demo Mode seeds HR Assistant, Finance Copilot and Procurement Agent.
- Confirm `requirements.txt` is committed.
- Confirm `.streamlit/config.toml` is committed.
- Confirm `.streamlit/secrets.toml` is not committed.
- Confirm `data/*.db` and `data/chroma/` are not committed.
- Set Streamlit Community Cloud main file path to `app.py`.
- Run the demo walkthrough in order: Dashboard, Agent Catalogue, Agent Details, Live Agent Audit, Analytics.

## Architecture

- Frontend: Streamlit
- Backend architecture: internal services plus optional FastAPI interface
- AI workflow: LangGraph-compatible workflow with deterministic Demo Mode evaluators
- Database: SQLite via SQLAlchemy
- Vector DB target: ChromaDB with deterministic Demo Mode seeding
- Charts: Plotly
- Deployment: Streamlit Community Cloud
