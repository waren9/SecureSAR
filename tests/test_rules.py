from src.detection.rule_engine import apply_rules, rules_to_frame
import pandas as pd


def test_apply_rules_basic():
    df = pd.DataFrame(
        {
            "customer_id": ["C1", "C2"],
            "total_amount": [200_000, 10_000],
            "deviation_score": [5.0, 0.1],
        }
    )
    results = apply_rules(df)
    rules_df = rules_to_frame(results)
    assert not rules_df.empty
    assert "C1" in rules_df["customer_id"].values

