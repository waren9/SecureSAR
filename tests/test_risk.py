from src.risk_scoring.risk_calculator import compute_risk_scores
import pandas as pd


def test_compute_risk_scores_shapes():
    features = pd.DataFrame(
        {
            "customer_id": ["C1", "C2"],
            "total_amount": [1000.0, 5000.0],
        }
    )
    rules_df = pd.DataFrame(
        {
            "customer_id": ["C1"],
            "rule_id": ["R1"],
            "description": [""],
        }
    )
    anomaly_scores = pd.Series([0.1, 0.9])
    cluster_df = features.assign(cluster=[0, 1])
    typologies = [{"customer_id": "C1", "typology": "Test"}]

    scores_df, typ_df = compute_risk_scores(features, rules_df, anomaly_scores, cluster_df, typologies)
    assert set(scores_df.columns) >= {"customer_id", "risk_score", "risk_band"}
    assert len(typ_df) == 1

