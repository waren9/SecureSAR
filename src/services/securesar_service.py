from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Any

import pandas as pd

from src.data_engineering.ingestion import load_raw_data
from src.data_engineering.validation import (
    validate_customers,
    validate_transactions,
    validate_alerts,
)
from src.data_engineering.feature_engineering import engineer_features
from src.detection.rule_engine import apply_rules, rules_to_frame
from src.detection.anomaly_detection import fit_isolation_forest
from src.detection.clustering import embed_and_cluster
from src.detection.typology_mapping import map_to_typologies
from src.risk_scoring.risk_calculator import compute_risk_scores
from src.explainability.audit_logger import AuditLogger, AuditEvent
from src.llm.narrative_generator import NarrativeGenerator


@dataclass
class Case:
    id: str
    customer_id: str
    risk_score: float
    risk_band: str
    typologies: List[str]
    triggered_rules: List[str]
    shap_values: Dict[str, float]


class SecureSarService:
    """
    High-level orchestration service that runs the SecureSAR decision pipeline
    and exposes case-centric helper methods for the FastAPI layer.
    """

    def __init__(self) -> None:
        self._cases: Dict[str, Case] = {}
        self._audit = AuditLogger()
        self._narrative = NarrativeGenerator()
        self._pipeline_ran = False

    def run_pipeline(self) -> None:
        """
        Run the full pipeline on the current raw data and cache case results.
        """
        customers, transactions, alerts = load_raw_data()
        customers = validate_customers(customers)
        transactions = validate_transactions(transactions)
        alerts = validate_alerts(alerts)

        features = engineer_features(customers, transactions)
        features_clustered, _ = embed_and_cluster(features)
        _, anomaly_scores = fit_isolation_forest(features)

        rule_results = apply_rules(features)
        rules_df = rules_to_frame(rule_results)

        typology_records = map_to_typologies(rules_df, anomaly_scores)
        risk_df, typology_df = compute_risk_scores(
            features_clustered, rules_df, anomaly_scores, features_clustered, typology_records
        )

        # Build cases keyed by a simple case id (here we use customer_id).
        cases: Dict[str, Case] = {}
        for _, row in risk_df.iterrows():
            cust_id = str(row["customer_id"])
            case_id = cust_id  # one case per customer for demo

            cust_typologies = typology_df[typology_df["customer_id"] == cust_id]["typology"].tolist()
            cust_rules = rules_df[rules_df["customer_id"] == cust_id]["rule_id"].tolist()

            # Simple "SHAP-like" contributions: treat components as feature attributions
            shap_values = {
                "rule_component": float(row.get("rule_score", 0.0)),
                "anomaly_component": float(row.get("anomaly_score", 0.0)),
                "cluster_component": float(row.get("cluster_score", 0.0)),
            }

            cases[case_id] = Case(
                id=case_id,
                customer_id=cust_id,
                risk_score=float(row["risk_score"]),
                risk_band=str(row["risk_band"]),
                typologies=cust_typologies,
                triggered_rules=cust_rules,
                shap_values=shap_values,
            )

        self._cases = cases
        self._pipeline_ran = True
        self._audit.log(
            AuditEvent(
                event_type="PIPELINE_RUN",
                actor="system",
                details={"cases": len(cases)},
            )
        )

    def _ensure_pipeline(self) -> None:
        if not self._pipeline_ran:
            self.run_pipeline()

    def list_high_risk_cases(self, min_risk: float = 0.8) -> List[Dict[str, Any]]:
        """
        Return a list of high-risk cases for the UI.
        """
        self._ensure_pipeline()
        out: List[Dict[str, Any]] = []
        for case in self._cases.values():
            if case.risk_score >= min_risk or case.risk_band == "High":
                out.append(
                    {
                        "id": case.id,
                        "customer_id": case.customer_id,
                        "risk_score": case.risk_score,
                        "risk_band": case.risk_band,
                    }
                )
        return out

    def get_case(self, case_id: str) -> Dict[str, Any] | None:
        """
        Retrieve a single case with risk explanation.
        """
        self._ensure_pipeline()
        case = self._cases.get(case_id)
        if not case:
            return None
        return {
            "id": case.id,
            "customer_id": case.customer_id,
            "risk_score": case.risk_score,
            "risk_band": case.risk_band,
            "typologies": case.typologies,
            "triggered_rules": case.triggered_rules,
            "shap_values": case.shap_values,
        }

    def generate_narrative(self, case_id: str, actor: str) -> str | None:
        """
        Generate a SAR narrative for the given case, log the action, and return the text.
        """
        self._ensure_pipeline()
        case = self._cases.get(case_id)
        if not case:
            return None

        evidence = {
            "case_id": case.id,
            "customer_id": case.customer_id,
            "risk_score": case.risk_score,
            "risk_band": case.risk_band,
            "typologies": case.typologies,
            "triggered_rules": case.triggered_rules,
        }
        narrative = self._narrative.generate(evidence)

        self._audit.log(
            AuditEvent(
                event_type="GENERATE_NARRATIVE",
                actor=actor,
                details={"case_id": case.id},
            )
        )
        return narrative

    def get_audit_log_for_case(self, case_id: str) -> List[Dict[str, Any]]:
        """
        Return audit events for a specific case by filtering the JSONL log.
        """
        self._ensure_pipeline()
        path = self._audit.path
        if not path.exists():
            return []
        rows: List[Dict[str, Any]] = []
        for line in path.read_text(encoding="utf-8").splitlines():
            try:
                rec = pd.json_normalize([line]).to_dict(orient="records")[0]
            except Exception:
                continue
            details = rec.get("details", {})
            # Details may be stored as a JSON string when normalized via pandas
            if isinstance(details, str):
                try:
                    import json as _json

                    details = _json.loads(details)
                except Exception:
                    details = {}
            if details.get("case_id") == case_id:
                rows.append(rec)
        return rows


service = SecureSarService()


__all__ = ["SecureSarService", "service"]

