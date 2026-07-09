# Sentinel Engineering Implementation Plan

Source of truth: `docs/PRD.md`

Product: Sentinel - Agent of Agents  
Tagline: Observe. Audit. Trust. Optimize.

## 1. Overall Architecture

Sentinel is an enterprise AgentOps Control Tower that observes, audits, governs and optimizes AI agents without replacing existing agents. The product should be implemented as a production-like hackathon application with a clear separation between frontend, backend, AI workflow orchestration, data persistence and evaluation agents.

High-level architecture:

```text
Enterprise Agent
    |
    v
Sentinel Gateway
    |
    v
FastAPI Backend
    |
    v
LangGraph Audit Workflow
    |
    +--> Hallucination Agent
    +--> Policy Agent
    +--> Cost Agent
    |
    v
Trust Score Aggregator
    |
    v
Recommendation Engine
    |
    v
Feedback Engine
    |
    v
SQLite + ChromaDB
    |
    v
Streamlit Dashboard
```

Primary runtime responsibilities:

- Streamlit provides the user-facing screens: Dashboard, Agent Catalogue, Agent Details, Live Audit and Analytics.
- FastAPI exposes stable application APIs for agents, audit runs, findings, trust scores, recommendations, feedback and analytics.
- LangGraph coordinates the audit workflow from captured run to dashboard update.
- SQLite stores structured application data.
- ChromaDB stores reference documents, policy context, evaluation evidence and semantic lookup material.
- OpenAI/Azure OpenAI powers evaluation, summarization and recommendation generation.
- Plotly renders metrics and trends for the Dashboard and Analytics screens.

The architecture should optimize for a credible hackathon demo while preserving clean module boundaries for future enterprise integrations such as Azure AI Foundry, Teams, Jira and Slack.

## 2. Folder Structure

Recommended repository structure:

```text
Sentinel/
  docs/
    PRD.md
    ENGINEERING_PLAN.md

  app/
    frontend/
      streamlit_app.py
      pages/
        dashboard.py
        agent_catalogue.py
        agent_details.py
        live_audit.py
        analytics.py
      components/
        metric_cards.py
        charts.py
        agent_table.py
        audit_timeline.py
        finding_panels.py
      state/
        session_state.py

    backend/
      main.py
      api/
        agents.py
        audit_runs.py
        recommendations.py
        feedback.py
        analytics.py
      schemas/
        agents.py
        audit_runs.py
        recommendations.py
        feedback.py
        analytics.py
      services/
        agent_catalogue_service.py
        audit_service.py
        trust_score_service.py
        recommendation_service.py
        feedback_service.py
        analytics_service.py
      repositories/
        agent_repository.py
        audit_run_repository.py
        recommendation_repository.py
        feedback_repository.py
        trust_score_repository.py
      core/
        config.py
        logging.py
        errors.py

    agents/
      graph.py
      state.py
      hallucination_agent.py
      policy_agent.py
      cost_agent.py
      trust_score_aggregator.py
      recommendation_engine.py
      feedback_engine.py
      prompts/
        hallucination.md
        policy.md
        cost.md
        recommendation.md

    models/
      database.py
      agent.py
      audit_run.py
      recommendation.py
      feedback.py
      trust_score.py
      policy_violation.py
      hallucination_finding.py
      user.py

    vectorstore/
      chroma_client.py
      collections.py
      seed_data.py

    demo/
      scenarios.py
      sample_agents.py
      sample_runs.py

    utils/
      ids.py
      time.py
      token_costs.py
      pii.py

  data/
    sentinel.db
    chroma/

  tests/
    backend/
    agents/
    frontend/

  requirements.txt
  README.md
  .env.example
```

For the first hackathon implementation, the project can keep the FastAPI backend and Streamlit frontend in the same repository and run them as separate processes or as a Streamlit-first app that calls service functions directly where Streamlit Community Cloud constraints require it. The module boundaries should still be preserved.

## 3. Database Design

Database: SQLite

The database should support the PRD tables exactly: Agent, AuditRun, Recommendation, Feedback, TrustScore, PolicyViolation, HallucinationFinding and Users.

### Agent

Stores registered enterprise AI agents.

Fields:

- `id`: primary key
- `name`: agent name, for example HR Assistant, Finance Copilot, Procurement Agent
- `description`: business description
- `owner_user_id`: foreign key to Users
- `business_unit`: owning team or department
- `agent_type`: assistant, copilot, workflow agent or other approved category
- `status`: active, inactive or under_review
- `created_at`
- `updated_at`

Relationships:

- One Agent has many AuditRun records.
- One Agent has many TrustScore records.
- One Agent belongs to one owner in Users.

### AuditRun

Stores each captured execution from an enterprise agent.

Fields:

- `id`: primary key
- `agent_id`: foreign key to Agent
- `input_text`: captured user input or task
- `output_text`: captured agent response
- `context_summary`: optional retrieved or business context summary
- `model_name`: model used by the enterprise agent, when available
- `prompt_tokens`
- `completion_tokens`
- `total_tokens`
- `estimated_cost`
- `status`: pending, running, completed or failed
- `started_at`
- `completed_at`
- `created_at`

Relationships:

- One AuditRun can have many PolicyViolation records.
- One AuditRun can have many HallucinationFinding records.
- One AuditRun can have many Recommendation records.
- One AuditRun can produce one or more TrustScore records.
- One AuditRun can have many Feedback records.

### Recommendation

Stores remediation recommendations produced by the Recommendation Engine.

Fields:

- `id`: primary key
- `audit_run_id`: foreign key to AuditRun
- `agent_id`: foreign key to Agent
- `recommendation_type`: policy, hallucination, cost, trust or operational
- `title`
- `description`
- `severity`: low, medium, high or critical
- `status`: open, accepted, dismissed or resolved
- `created_at`
- `updated_at`

### Feedback

Stores Human Feedback from target users and reviewers.

Fields:

- `id`: primary key
- `audit_run_id`: foreign key to AuditRun
- `agent_id`: foreign key to Agent
- `user_id`: foreign key to Users
- `rating`: numeric or categorical feedback
- `comment`
- `decision`: approve, reject, needs_review or resolved
- `created_at`

### TrustScore

Stores calculated trust scoring snapshots.

Fields:

- `id`: primary key
- `agent_id`: foreign key to Agent
- `audit_run_id`: optional foreign key to AuditRun
- `overall_score`: 0 to 100
- `hallucination_score`: 0 to 100
- `policy_score`: 0 to 100
- `cost_score`: 0 to 100
- `feedback_score`: 0 to 100
- `calculation_notes`
- `created_at`

Score interpretation:

- 80 to 100: trusted
- 60 to 79: watch
- 0 to 59: at risk

### PolicyViolation

Stores policy and PII violations detected by the Policy Evaluator.

Fields:

- `id`: primary key
- `audit_run_id`: foreign key to AuditRun
- `agent_id`: foreign key to Agent
- `violation_type`: PII, compliance, security, policy or other approved type
- `description`
- `evidence`
- `severity`: low, medium, high or critical
- `policy_status`: PASS, WARN or FAIL
- `created_at`

### HallucinationFinding

Stores hallucination detection results from the Hallucination Evaluator.

Fields:

- `id`: primary key
- `audit_run_id`: foreign key to AuditRun
- `agent_id`: foreign key to Agent
- `claim`
- `evidence`
- `finding_status`: supported, unsupported or uncertain
- `confidence`
- `description`
- `created_at`

### Users

Stores users who own agents or provide feedback.

Fields:

- `id`: primary key
- `name`
- `email`
- `role`: AI Platform Owner, CIO/CTO, Compliance Officer, AI Developer or Product Manager
- `created_at`
- `updated_at`

### ChromaDB Collections

ChromaDB should complement SQLite rather than replace it.

Recommended collections:

- `policy_knowledge_base`: enterprise policies, PII rules and compliance guidance.
- `agent_run_evidence`: indexed run context and output evidence used by the Hallucination Evaluator.
- `recommendation_memory`: prior recommendations and resolved feedback for the Feedback Loop.

## 4. Backend Architecture

Backend: FastAPI

The backend should expose application APIs and isolate business logic from UI rendering.

### API Layer

Core routes:

- `GET /health`: service health.
- `GET /agents`: list Agent Catalogue records.
- `POST /agents`: register Agent.
- `GET /agents/{agent_id}`: Agent Details data.
- `GET /agents/{agent_id}/audit-runs`: audit history for one Agent.
- `POST /audit-runs`: submit an agent execution to Sentinel Gateway.
- `GET /audit-runs/{audit_run_id}`: full audit result.
- `POST /audit-runs/{audit_run_id}/evaluate`: run Live Agent Audit workflow.
- `GET /recommendations`: list Recommendation records.
- `POST /feedback`: submit Human Feedback.
- `GET /analytics/overview`: Dashboard metrics.
- `GET /analytics/trends`: Analytics charts.

### Service Layer

Services should hold business logic:

- `AgentCatalogueService`: creates, updates and reads Agent records.
- `AuditService`: captures runs, starts evaluations and returns audit details.
- `TrustScoreService`: calculates Enterprise Trust Score and per-agent trust scores.
- `RecommendationService`: creates remediation recommendations.
- `FeedbackService`: records Human Feedback and updates downstream scoring signals.
- `AnalyticsService`: calculates Success Metrics for Dashboard and Analytics.

### Repository Layer

Repositories should isolate SQLite persistence and keep SQL or ORM-specific behavior out of services.

Repository responsibilities:

- Create and query PRD entities.
- Keep transactions explicit around audit workflow writes.
- Avoid leaking database models into Streamlit views.

### Backend Data Contracts

Pydantic schemas should define request and response contracts for:

- Agent registration
- AuditRun capture
- HallucinationFinding output
- PolicyViolation output
- TrustScore output
- Recommendation output
- Feedback submission
- Analytics metrics

## 5. Frontend Architecture

Frontend: Streamlit

The frontend should feel like an enterprise control tower, not a marketing page. The first screen should be the usable Dashboard.

### Frontend Principles

- Preserve approved business terminology exactly.
- Make the core journey visible: Register Agent -> Agent Executes -> Sentinel Captures Run -> Hallucination Check -> Policy Check -> Cost Analysis -> Trust Score -> Recommendations -> Human Feedback -> Dashboard Updated.
- Prioritize dense, scannable operational views for AI Platform Owners, Compliance Officers and AI Developers.
- Use Plotly for charts and trend analysis.
- Keep Streamlit page files thin; delegate data access to backend clients or service adapters.

### Shared Components

Recommended shared Streamlit components:

- Metric cards for Enterprise Trust Score, Hallucination Rate, PII Incidents, Average Cost per Run, Policy Violations and Agent Reuse.
- Agent table for Agent Catalogue.
- Audit timeline for Live Agent Audit.
- Finding panels for HallucinationFinding and PolicyViolation records.
- Recommendation list grouped by severity and status.
- Feedback form for Human Feedback.

### State Management

Use Streamlit session state for:

- Selected Agent
- Selected AuditRun
- Active demo scenario
- Temporary form state
- Live Agent Audit progress display

Persistent state belongs in SQLite, not Streamlit session state.

## 6. LangGraph Workflow

LangGraph should implement the PRD AI Architecture and user journey as an explicit graph.

### Graph State

Recommended graph state:

- `agent_id`
- `audit_run_id`
- `input_text`
- `output_text`
- `context_summary`
- `policy_context`
- `hallucination_findings`
- `policy_violations`
- `cost_analysis`
- `trust_score`
- `recommendations`
- `feedback_signals`
- `errors`

### Nodes

1. `sentinel_gateway`
   - Normalizes captured Enterprise Agent execution.
   - Loads Agent metadata and AuditRun details.
   - Prepares data for evaluators.

2. `hallucination_agent`
   - Implements Hallucination Evaluator.
   - Extracts claims from output.
   - Compares claims against available context and ChromaDB evidence.
   - Produces HallucinationFinding records.

3. `policy_agent`
   - Implements Policy Evaluator.
   - Checks for PII, compliance and policy violations.
   - Uses ChromaDB policy context.
   - Produces PolicyViolation records with PASS, WARN or FAIL status.

4. `cost_agent`
   - Implements Cost Optimizer.
   - Calculates estimated cost from token usage.
   - Detects excessive tokens and inefficient runs.
   - Produces cost optimization signals.

5. `trust_score_aggregator`
   - Implements Trust Score Engine.
   - Combines hallucination, policy, cost and feedback signals.
   - Produces TrustScore records.

6. `recommendation_engine`
   - Implements Recommendation Engine.
   - Generates remediation recommendations from findings and trust score.
   - Prioritizes high-impact actions for production readiness.

7. `feedback_engine`
   - Implements Feedback Loop.
   - Incorporates Human Feedback into future scoring and recommendations.
   - Stores feedback-derived signals for Analytics.

8. `dashboard_update`
   - Persists final workflow outputs.
   - Makes results available to Dashboard, Agent Details, Live Audit and Analytics.

### Edges

Recommended flow:

```text
sentinel_gateway
    -> hallucination_agent
    -> policy_agent
    -> cost_agent
    -> trust_score_aggregator
    -> recommendation_engine
    -> feedback_engine
    -> dashboard_update
```

For the hackathon demo, the Hallucination Agent, Policy Agent and Cost Agent can run sequentially for simpler traceability. If time allows, they can be parallelized before Trust Score Aggregator.

## 7. AI Agent Responsibilities

### Hallucination Agent

Purpose: reduce hallucinations and support production readiness.

Responsibilities:

- Identify factual claims in Enterprise Agent output.
- Compare claims against provided context and ChromaDB evidence.
- Mark claims as supported, unsupported or uncertain.
- Produce HallucinationFinding records.
- Contribute to Hallucination Rate and Trust Score Engine.

Demo alignment:

- Detect that Finance Copilot hallucinates revenue.

### Policy Agent

Purpose: detect policy and PII violations.

Responsibilities:

- Scan input and output for PII.
- Validate content against policy context.
- Classify violations by type and severity.
- Produce PolicyViolation records.
- Return PASS, WARN or FAIL status.
- Contribute to PII Incidents, Policy Violations and Trust Score Engine.

Demo alignment:

- Detect that HR Assistant leaks PII and mark Policy FAIL.

### Cost Agent

Purpose: reduce operational cost and improve cost efficiency.

Responsibilities:

- Calculate prompt, completion and total token usage.
- Estimate run cost.
- Detect excessive tokens.
- Suggest lower-cost operational patterns.
- Contribute to Average Cost per Run and Trust Score Engine.

Demo alignment:

- Detect that Procurement Agent uses excessive tokens and suggest cost optimization.

### Trust Score Aggregator

Purpose: provide centralized trust scoring.

Responsibilities:

- Convert evaluator outputs into normalized sub-scores.
- Calculate overall trust score.
- Store TrustScore records.
- Support Enterprise Trust Score rollups.
- Flag agents as trusted, watch or at risk.

### Recommendation Engine

Purpose: provide remediation recommendations.

Responsibilities:

- Convert findings into clear action items.
- Prioritize by severity and business impact.
- Recommend policy remediation, hallucination mitigation and cost optimization.
- Track recommendation status.

### Feedback Engine

Purpose: close the Feedback Loop.

Responsibilities:

- Capture Human Feedback.
- Feed feedback into future trust scoring.
- Track approval, rejection, review and resolution decisions.
- Support Dashboard Updated state after feedback.

## 8. UI Screen Hierarchy

### Dashboard

Primary first screen for the AgentOps Control Tower.

Content:

- Enterprise Trust Score
- Hallucination Rate
- PII Incidents
- Average Cost per Run
- Policy Violations
- Agent Reuse
- Top at-risk agents
- Recent Live Agent Audit results
- Recommendation summary

Primary actions:

- Start Live Agent Audit
- View Agent Catalogue
- Open Analytics

### Agent Catalogue

Purpose: answer which agents exist and who owns them.

Content:

- Agent list
- Owner
- Business unit
- Status
- Latest Trust Score
- Latest policy status
- Latest cost signal

Primary actions:

- Register Agent
- Open Agent Details
- Start audit for selected Agent

### Agent Details

Purpose: provide a single-agent governance view.

Content:

- Agent metadata
- Owner and business unit
- Trust Score history
- AuditRun history
- HallucinationFinding history
- PolicyViolation history
- Recommendation history
- Feedback history

Primary actions:

- Run Live Agent Audit
- Submit Human Feedback
- Resolve Recommendation

### Live Audit

Purpose: show Sentinel Captures Run and evaluator progress.

Content:

- Agent selector
- Input and output capture form
- Demo scenario selector for HR Assistant, Finance Copilot and Procurement Agent
- Step-by-step audit progress
- Hallucination Check result
- Policy Check result
- Cost Analysis result
- Trust Score result
- Recommendations

Primary actions:

- Capture Run
- Run evaluation
- Submit Human Feedback

### Analytics

Purpose: track governance and optimization outcomes.

Content:

- Enterprise Trust Score trends
- Hallucination Rate trends
- PII Incidents over time
- Average Cost per Run trends
- Policy Violations by severity
- Agent Reuse by agent
- Recommendation status distribution

Primary actions:

- Filter by agent, owner, business unit and date range
- Drill into Agent Details

## 9. Deployment Architecture

Target deployment: Streamlit Community Cloud

Recommended hackathon deployment:

```text
Streamlit Community Cloud
    |
    +--> Streamlit frontend
    |
    +--> Local application services imported by Streamlit
    |
    +--> SQLite database file in app storage
    |
    +--> ChromaDB persistent directory in app storage
    |
    +--> OpenAI/Azure OpenAI via secrets
```

Because Streamlit Community Cloud is the target deployment, the simplest reliable hackathon path is to package the application as a Streamlit app that preserves backend/service/agent boundaries internally. FastAPI can still be developed as the backend interface and run locally, but the deployed demo may call service functions directly if running a separate API service is not practical on Streamlit Community Cloud.

Local development architecture:

```text
Developer machine
    |
    +--> FastAPI backend on localhost
    |
    +--> Streamlit frontend on localhost
    |
    +--> SQLite
    |
    +--> ChromaDB
    |
    +--> OpenAI/Azure OpenAI
```

Environment configuration:

- `OPENAI_API_KEY` or Azure OpenAI equivalent
- `OPENAI_MODEL` or Azure deployment name
- `DATABASE_URL` for SQLite
- `CHROMA_DB_PATH`
- Optional demo mode flag for deterministic hackathon scenarios

Deployment constraints:

- Avoid external services that require complex provisioning during the hackathon.
- Seed demo data on first run.
- Keep all required secrets in Streamlit secrets management.
- Provide deterministic demo scenarios so the product works even if live LLM calls are rate-limited.

## 10. Development Phases

### Phase 1: Foundation

Goals:

- Establish repository structure.
- Add configuration, logging and database setup.
- Define database models for Agent, AuditRun, Recommendation, Feedback, TrustScore, PolicyViolation, HallucinationFinding and Users.
- Add seed data for HR Assistant, Finance Copilot and Procurement Agent.

Deliverable:

- Application can initialize SQLite and show seeded Agent Catalogue data.

### Phase 2: Backend Core

Goals:

- Implement Agent Catalogue APIs and services.
- Implement AuditRun capture.
- Implement analytics service for baseline Success Metrics.
- Add repository layer.

Deliverable:

- FastAPI can register agents, capture runs and return Dashboard metrics.

### Phase 3: LangGraph Workflow

Goals:

- Implement graph state and nodes.
- Add Hallucination Agent.
- Add Policy Agent.
- Add Cost Agent.
- Add Trust Score Aggregator.
- Add Recommendation Engine.
- Add Feedback Engine.

Deliverable:

- A captured run can move through the full Sentinel workflow and produce persisted findings, trust score and recommendations.

### Phase 4: Streamlit UI

Goals:

- Build Dashboard.
- Build Agent Catalogue.
- Build Agent Details.
- Build Live Audit.
- Build Analytics.
- Add Plotly charts.

Deliverable:

- End-to-end user journey works from Streamlit.

### Phase 5: Demo Scenario Polish

Goals:

- Implement deterministic demo scenarios:
  - HR Assistant leaks PII -> Policy FAIL.
  - Finance Copilot hallucinates revenue -> Hallucination detected.
  - Procurement Agent uses excessive tokens -> Cost optimization suggested.
- Add clear visual states for PASS, WARN and FAIL.
- Validate Success Metrics update after Human Feedback.

Deliverable:

- Hackathon demo can be completed reliably without manual database edits.

### Phase 6: Production-Like Hardening

Goals:

- Add tests for services and LangGraph nodes.
- Add error handling for failed LLM calls.
- Add fallback deterministic evaluators for demo reliability.
- Add README setup instructions.
- Add `.env.example`.

Deliverable:

- Project is stable enough for judging, local development and future extension.

## 11. Risks

### Streamlit Community Cloud and FastAPI Runtime

Risk: Streamlit Community Cloud may not support running a separate long-lived FastAPI process cleanly.

Mitigation: Preserve FastAPI-compatible service boundaries, but allow Streamlit to call application services directly for the deployed hackathon version.

### LLM Reliability

Risk: LLM calls may be slow, rate-limited or inconsistent during a live demo.

Mitigation: Support deterministic demo mode for the three PRD demo scenarios and use LLM calls where available.

### Hallucination Detection Accuracy

Risk: Hallucination detection depends on available evidence and context.

Mitigation: Store explicit demo evidence in ChromaDB and classify unsupported claims conservatively.

### Policy Evaluation Scope

Risk: Enterprise policy validation can become too broad for hackathon scope.

Mitigation: Start with PII, compliance and policy examples that map directly to the PRD, then expand later.

### Trust Score Explainability

Risk: Users may not trust a numeric score without explanation.

Mitigation: Store calculation notes and sub-scores for hallucination, policy, cost and feedback.

### SQLite Concurrency

Risk: SQLite is sufficient for a hackathon but limited for high-concurrency production use.

Mitigation: Keep repository abstractions clean so a later database migration is straightforward.

### Product Terminology Drift

Risk: Engineering implementation could accidentally rename approved concepts.

Mitigation: Use PRD terminology exactly in model names, UI labels, docs and route descriptions.

## 12. Assumptions

- Sentinel remains the product name.
- The approved positioning is Sentinel - Agent of Agents.
- The approved tagline is Observe. Audit. Trust. Optimize.
- The core modules remain Agent Catalogue, Live Agent Audit, Hallucination Evaluator, Policy Evaluator, Cost Optimizer, Trust Score Engine, Recommendation Engine and Feedback Loop.
- Streamlit is the required frontend for the hackathon.
- FastAPI is the intended backend architecture, even if the deployed Streamlit Community Cloud version calls services directly for runtime simplicity.
- LangGraph is required for the AI workflow.
- OpenAI/Azure OpenAI is available through secrets.
- ChromaDB is used for vector storage and semantic evidence lookup.
- SQLite is sufficient for hackathon persistence.
- Plotly is used for charts.
- The first demo must support HR Assistant, Finance Copilot and Procurement Agent exactly as described in the PRD.
- The initial implementation should optimize for a reliable hackathon demo while keeping production-like separation of frontend, backend, agents, services, models and utilities.
