-- Minimal schema for SecureSAR when using PostgreSQL.

CREATE TABLE IF NOT EXISTS sar_case (
    id TEXT PRIMARY KEY,
    customer_id TEXT NOT NULL,
    risk_score DOUBLE PRECISION NOT NULL,
    risk_band TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE IF NOT EXISTS sar_audit_event (
    id SERIAL PRIMARY KEY,
    case_id TEXT,
    event_type TEXT NOT NULL,
    actor TEXT NOT NULL,
    details JSONB,
    created_at TIMESTAMPTZ DEFAULT now()
);

