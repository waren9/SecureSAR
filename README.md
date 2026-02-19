SAR Decision Intelligence Platform
==================================

This repository contains a modular, end‑to‑end **Suspicious Activity Report (SAR) Decision Intelligence** pipeline designed for regulated banking environments. It combines:

- **Synthetic data generation** (no real customer data required)
- **Data engineering & feature engineering**
- **Rule‑based, ML‑based, and anomaly‑based detection**
- **Risk scoring with configurable weights**
- **Explainability & full audit trails**
- **RAG + LLM narrative generation (with safe fallbacks)**
- **Security & governance layer** (RBAC, PII masking, prompt guardrails)
- **Streamlit analyst UI** for human review and approval

The code is structured so you can:

- Run the full pipeline end‑to‑end on synthetic data
- Plug in real data sources later (DB or batch files)
- Swap / upgrade models while keeping the same interfaces
- Demonstrate **governance‑first, regulator‑ready AI** for SARs

---

Project Layout
--------------

```text
sar-decision-intelligence/
├── data/
│   ├── raw/                     # Synthetic / ingested CSVs
│   ├── processed/               # Engineered features, scores, clusters
│   └── synthetic_generator.py   # Synthetic data framework
│
├── src/
│   ├── data_engineering/        # Ingestion, validation, features, preprocessing
│   ├── detection/               # Rules, anomaly detection, clustering, typologies
│   ├── risk_scoring/            # Risk calculator + YAML weights
│   ├── explainability/          # SHAP, decision traces, audit logger
│   ├── llm/                     # Prompt templates, RAG pipeline, narrative generator
│   ├── governance/              # Role‑based access, masking policies, env guardrails
│   ├── security/                # Concrete RBAC, PII masking, LLM prompt guard
│   └── utils/                   # Config, helpers
│
├── ui/
│   ├── streamlit_app.py         # Analyst UI (review + approve SAR)
│   └── visualization.py         # Risk and cluster visualizations
│
├── database/
│   ├── schema.sql               # Minimal schema for SAR cases
│   └── db_connector.py          # DB helper (SQLite by default)
│
├── tests/                       # Pytest tests
├── requirements.txt
├── Dockerfile
└── README.md
```

---

Conceptual Architecture
-----------------------

### 1. Synthetic Data Layer

- `data/synthetic_generator.py` builds realistic but **fully synthetic**:
  - `transactions.csv`
  - `customers.csv`
  - `alerts.csv`
- Supports configurable volume (e.g. 100k–5M transactions, 5k–50k customers).
- Injects known AML patterns: structuring, rapid fund movement, dormant reactivation, high‑risk corridors, etc.

### 2. Data Engineering Layer (`src/data_engineering`)

- `ingestion.py`:
  - Loads CSVs (or DB tables later) into pandas DataFrames.
- `validation.py`:
  - Schema checks, duplication checks, type casting, basic sanity rules.
- `feature_engineering.py`:
  - Behavioural features: velocity metrics, distinct counterparties, deviation scores.
- `preprocessing.py`:
  - Standardization, encoding, train/test splits.

Output: **feature‑rich, analysis‑ready tables** in `data/processed/`.

### 3. Detection Layer (`src/detection`)

- `rule_engine.py`:
  - Deterministic AML rules (e.g. large cash deposits, rapid in/out, high‑risk corridors).
  - Outputs triggered rule IDs per account / alert.
- `anomaly_detection.py`:
  - Isolation Forest‑based anomaly scores.
- `clustering.py`:
  - t‑SNE + K‑Means / DBSCAN customer‑level clusters and drift indicators.
- `typology_mapping.py`:
  - Maps rule + anomaly patterns to human‑readable AML typologies.

### 4. Risk Scoring Layer (`src/risk_scoring`)

- `risk_calculator.py`:
  - Combines rule triggers, anomaly scores, clusters and typologies into a single risk score.
- `score_weights.yaml`:
  - Stores configurable weights and thresholds (e.g. rule weight, anomaly weight, cluster weight).

Output: `risk_scores.csv` in `data/processed/`.

### 5. Explainability & Audit Layer (`src/explainability`)

- `shap_explainer.py`:
  - Computes SHAP values for tree‑based models.
- `decision_trace.py`:
  - Extracts transparent decision paths (e.g. from a decision tree model).
- `audit_logger.py`:
  - Writes JSON logs capturing:
    - Inputs and outputs of the detection and risk layers
    - Triggered rules
    - Model scores and SHAP explanations
    - User actions, prompts, and LLM responses

All logs are **machine‑readable and regulator‑friendly**.

### 6. LLM & RAG Layer (`src/llm`)

- `prompt_template.txt`:
  - Defines a **strict SAR drafting template** and guardrailed instructions for the LLM.
- `rag_pipeline.py`:
  - Lightweight RAG over local documents (SAR templates, regulatory snippets).
- `narrative_generator.py`:
  - Builds a SAR narrative from structured evidence.
  - Uses:
    - A real LLM if configured (`OPENAI_API_KEY` or pluggable provider), **or**
    - A deterministic fallback template when no LLM credentials are available.

### 7. Governance & Security Layers

#### Governance (`src/governance`)

- `role_based_access.py`:
  - Business‑level RBAC: Analyst, Supervisor, Admin, Regulator.
- `data_masking.py`:
  - High‑level masking policies (what should be masked where).
- `environment_guardrails.py`:
  - On‑prem vs cloud constraints, outbound call restrictions, deployment‑time controls.

#### Security (`src/security`)

Concrete, testable security controls:

- `rbac.py`:
  - Fine‑grained permission checks (e.g. *can_edit_sar*, *can_modify_risk_logic*).
- `pii_masking.py`:
  - Deterministic tokenization / masking of PII (accounts, PAN, Aadhaar, phone, address).
- `prompt_guard.py`:
  - Protects the LLM from:
    - Prompt injection
    - Off‑topic or policy‑violating output
  - Enforces:
    - Fixed system prompt invariants
    - Output validation (evidence IDs, no demographics, no URLs, etc.)

Together, these layers ensure the system is **not just smart, but safe**.

### 8. UI & Database Layers

- `ui/streamlit_app.py`:
  - Analyst‑friendly UI for:
    - Viewing high‑risk alerts
    - Inspecting evidence and explanations
    - Editing SAR drafts
    - Submitting SARs for approval
- `ui/visualization.py`:
  - Helper functions for visualizing risk scores and clusters.
- `database/schema.sql` & `database/db_connector.py`:
  - Minimal SQLite schema and connection helpers for storing:
    - SAR drafts
    - Final SARs
    - User actions and approvals

---

Quickstart
----------

### 1. Install Dependencies

From the project root (`sar-decision-intelligence/`):

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Generate Synthetic Data

```bash
python -m data.synthetic_generator
```

This populates `data/raw/` with `customers.csv`, `transactions.csv`, and `alerts.csv`.

### 3. Run the Detection & Scoring Pipeline

```bash
python -m src.main
```

This will:

- Ingest and validate the raw CSVs
- Generate features and processed datasets
- Run rules, anomaly detection, and clustering
- Compute risk scores into `data/processed/risk_scores.csv`
- Produce structured evidence and audit logs

### 4. Launch the Analyst UI

```bash
streamlit run ui/streamlit_app.py
```

You can then:

- Browse high‑risk entities
- Inspect structured evidence
- Review and edit SAR drafts
- Approve SARs (stored in the local SQLite DB)

---

Configuration
-------------

Key configuration lives in `src/utils/config.py`:

- Data paths (raw & processed)
- Model parameters (e.g. contamination for Isolation Forest)
- Risk scoring weights and thresholds
- LLM provider & model name

Override defaults using environment variables where appropriate.

---

LLM & RAG Configuration
-----------------------

By default, the system will **not** call any external LLM APIs unless you configure them.

- Set `OPENAI_API_KEY` (or another provider’s key) to enable real LLM calls.
- When no key is present, `narrative_generator.py` falls back to a **deterministic, template‑based narrative** using only structured evidence.
- RAG is implemented in a lightweight, local way so the project runs without extra infrastructure.

This design keeps the project:

- Easy to run on a laptop
- Safe for demos
- Ready to be upgraded to enterprise LLM infrastructure later

---

Security & Compliance Posture
-----------------------------

The **Security Layer** focuses on:

1. **Role‑based control over actions**
2. **Protection of PII in UI, logs, and prompts**
3. **Safe, constrained use of LLMs**
4. **Domain boundary protection for data flows**
5. **End‑to‑end auditability**

All security‑relevant functions are grouped in:

- `src/security/` for concrete, code‑level controls
- `src/governance/` for higher‑level policies and environment constraints

You can extend these modules to plug into your own IAM, KMS, or SIEM systems.

---

Running Tests
-------------

```bash
pytest -q
```

The test suite focuses on:

- Rule engine behaviour
- Risk scoring logic
- LLM narrative generation (including the safe fallback path)

---

Next Steps
----------

- Connect to a real database instead of CSVs.
- Refine rule sets and typology mapping to your institution.
- Replace the stub LLM integration with your preferred provider (OpenAI, Bedrock, local models, etc.).
- Integrate with your existing case management system.

The current codebase is intentionally **modular and extensible** to support these upgrades.

---

SecureSAR Platform Architecture (Full Stack)
-------------------------------------------

The SecureSAR platform extends the core SAR decision pipeline into a full stack system with:

- **React frontend**
- **FastAPI backend (API & orchestration)**
- **SecureSAR Python framework (this repo)**
- **External services** (PostgreSQL, OpenSearch, Amazon S3, Amazon Bedrock)

### Box-Based Architecture Diagram

```text
+---------------------------------------------------------------+
|                        FRONTEND LAYER                        |
|                     (React Web Application)                  |
|  - Analyst dashboard                                         |
|  - SAR draft editor                                          |
|  - Risk explanation & SHAP view                              |
|  - Audit log viewer                                          |
|  [HTTP/JSON]                                                 |
+-------------------------------|-------------------------------+
                                v
+---------------------------------------------------------------+
|                   API & ORCHESTRATION LAYER                   |
|                         (FastAPI)                             |
|  - API gateway / routing                                      |
|  - AuthN/AuthZ integration (JWT / RBAC hooks)                 |
|  - Request validation & response formatting                   |
|  - Orchestration of SecureSAR workflows                       |
|  - Calls into Python SecureSAR services                       |
|  [Python function calls]                                      |
+-------------------------------|-------------------------------+
                                v
+---------------------------------------------------------------+
|            CORE DECISION FRAMEWORK & AI (SecureSAR)          |
|                        (Python)                              |
|  - Data engineering (ETL, features)                          |
|  - Detection: rules, anomaly detection, clustering           |
|  - Risk scoring (scikit-learn)                               |
|  - Explainability (SHAP, decision traces)                    |
|  - SecureSAR governance & security (RBAC, masking, guards)   |
|  - LLM orchestration (Amazon Bedrock, RAG)                   |
|                                                               |
|  Internal flow:                                               |
|    Ingested data -> Features -> Rules/Models -> Risk scores  |
|    -> SHAP / explanations -> Evidence JSON                   |
|    -> Bedrock LLM (SAR narrative)                            |
+-------------------------------|-------------------------------+
                                v
+---------------------------------------------------------------+
|                 DATA STORAGE & EXTERNAL SERVICES             |
|                                                               |
|  PostgreSQL   - SAR cases, decisions, audit logs             |
|  OpenSearch   - SAR templates, regulatory text (RAG corpus)  |
|  Amazon S3    - SAR PDFs, evidence bundles                   |
|  Amazon Bedrock - LLM for SAR narratives (inputs: evidence)  |
+---------------------------------------------------------------+
```

### Explicit Data Flow

1. **React UI → FastAPI**
   - Analyst opens the web app and:
     - Requests a list of high‑risk cases.
     - Opens a specific case with risk explanation.
     - Requests SAR narrative generation.
   - React sends **HTTP/JSON** requests to FastAPI endpoints:
     - `GET /api/cases/high-risk`
     - `GET /api/cases/{case_id}`
     - `POST /api/cases/{case_id}/generate-sar`

2. **FastAPI → SecureSAR Python Core**
   - FastAPI authenticates the user and checks RBAC via SecureSAR security layer.
   - FastAPI orchestrates calls to Python services:
     - `SecureSarService.run_full_pipeline(...)`
     - `SecureSarService.get_case_with_explanations(case_id)`
     - `SecureSarService.generate_sar_narrative(case_id)`

3. **SecureSAR Core → Risk Models + SHAP**
   - The service uses the modules in `src/`:
     - `data_engineering/` for ingestion and features.
     - `detection/` for rules, anomaly detection, and clustering.
     - `risk_scoring/` for a scikit‑learn‑based risk model.
     - `explainability/` (SHAP + decision traces) for per‑case explanations.
   - Outputs:
     - Risk scores
     - Triggered rules
     - SHAP value vectors
     - Decision traces
     - Structured **evidence JSON**.

4. **SecureSAR Core → Amazon Bedrock (LLM)**
   - SecureSAR builds a **strict, evidence‑only prompt** using:
     - Evidence JSON
     - Retrieved templates and regulations (via RAG / OpenSearch)
     - A fixed system prompt from `prompt_template.txt`
   - The Bedrock client is invoked (or a local fallback is used in dev).
   - Bedrock returns a SAR narrative **constrained to the provided evidence**.

5. **SecureSAR Core → Data Stores**
   - **PostgreSQL**:
     - Persists SAR cases, risk scores, explanations, and audit logs.
   - **OpenSearch**:
     - Stores SAR templates, guidance notes, and regulatory text for retrieval.
   - **Amazon S3**:
     - Stores generated SAR PDFs and packaged evidence bundles.

6. **FastAPI → React UI**
   - FastAPI formats the combined outputs into clean JSON payloads:
     - Case metadata + risk score
     - List of triggered rules and SHAP explanations
     - SAR narrative draft
     - Audit log excerpts
   - React renders:
     - Risk heatmaps and SHAP breakdowns
     - Editable SAR draft
     - Full audit trace for compliance review.

This layered design keeps **React**, **FastAPI**, and the **SecureSAR decision framework** decoupled while ensuring the whole system is auditable, explainable, and safe for regulated SAR workflows.

