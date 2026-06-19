# Enterprise Deployment Architecture: Asynchronous Event-Driven AI Agent

This document outlines the production-grade target deployment architecture for the **Expense Management Dashboard**, built as part of the *Kaggle 5-Day AI Agents: Intensive Vibe Coding Course with Google*.

While the project has been rigorously validated and executed locally using an in-memory session simulation via FastAPI and Uvicorn, its cloud-native design is built for seamless serverless deployment to Google Cloud Platform (GCP).

---

## 🏛️ Architecture Overview

The system transitions traditional, fragile synchronous AI request/response chains into a resilient, **Asynchronous Event-Driven Topology** embedded with a **Human-in-the-Loop (HITL)** governance gate.

### 1. Ingestion Layer (Google Cloud Pub/Sub)

- **Mechanism:** Employee expense payloads are asynchronously published to a Google Cloud Pub/Sub topic instead of hitting the agent runtime via blocking REST endpoints.
- **Resilience Profile:** This architecture decouples ingestion from LLM processing speed, safely absorbing massive spikes in transaction volumes, preventing timeouts, and isolating failures through native message retry mechanisms.

### 2. Processing Layer (Vertex AI Agent Runtime)

- **Mechanism:** The containerized agent execution engine processes incoming event notifications pushed from the Pub/Sub subscription.
- **Deterministic Policy Gates:**
  - Expenses under **$100** trigger automatic processing paths, resolving instantly without human overhead.
  - Expenses **>= $100** are actively intercepted. The execution state context is captured, frozen, and securely persisted within the Vertex AI Session Service.

### 3. Serverless Governance Interface (Google Cloud Run)

- **Mechanism:** The standalone management dashboard is packaged into an OCI-compliant container via Cloud Build and deployed to **Google Cloud Run**.
- **Operational Efficiency:** Cloud Run implements automatic scaling down to absolute zero instances during periods of inactivity, dropping compute cost overhead to $0.00.
- **State Management:** The FastAPI backend communicates natively with the Session Service via the Google ADK, querying unresolved `adk_request_input` interrupts to render them as interactive glassmorphic cards for managers.
- **State Resumption:** Upon manager approval or rejection, a secure payload is sent to unfreeze and resume the agent's execution loop context safely under a strict system boundary.
- **Dead-Letter Queue (DLQ):** Integrated `expense-reports-dead-letter` to intercept malformed data or repeating parsing failures, protecting the core processing loop from poison-pill blockages

---

## 🔐 Zero-Trust Identity and Access Management (IAM)

To enforce strict compliance with the **Principle of Least Privilege (PoLP)**, the Cloud Run container operates under an explicitly isolated **Runtime Service Account** rather than using default project credentials.

### Role Configuration Bindings

| Infrastructure Target | Assigned Identity | IAM Role Assignment | Operational Boundary |
| :--- | :--- | :--- | :--- |
| **Manager Dashboard Container** | `expense-manager-dashboard@[PROJECT_ID].iam.gserviceaccount.com` | `roles/aiplatform.user` | Grants permission to scan active session memory, fetch interrupt IDs, and resume/terminate paused Agent Runtime loops. |
| **Pub/Sub Push Invoker** | `pubsub-invoker@[PROJECT_ID].iam.gserviceaccount.com` | `roles/aiplatform.user` | Grants the Pub/Sub subscription permission to mint OIDC tokens and securely POST unwrapped payloads directly to the Agent Runtime API. |

---

## ⚙️ Environment Decoupling

The codebase relies strictly on Twelve-Factor App methodologies, keeping logic entirely clean and decoupled from infrastructure state variables. The following keys are injected into the runtime space upon service deployment:

```bash
# Target Project Identifier
GOOGLE_CLOUD_PROJECT="enterprise-agent-security-lab"

# Pointer to Deployed Agent Context
AGENT_RUNTIME_ID="mock-runtime-region-global-12345"
```

---

## 🛠️ Local Verification & Development Trace

For local verification, mocking, and zero-cost debugging, the architecture is simulated using:

- **FastAPI Router Engine:** Mimics the target REST interfaces of Cloud Run.
- **In-Memory Session Arrays:** Models the asynchronous pipeline states of Vertex AI and Pub/Sub.
- **Uvicorn Web Worker:** Serves the frontend locally at `http://127.0.0.1:8000`.

To run the local verification suite:

```bash
uv add fastapi uvicorn
uv run uvicorn main:app --reload
```