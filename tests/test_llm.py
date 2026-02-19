from src.llm.narrative_generator import NarrativeGenerator


def test_narrative_generator_fallback():
    gen = NarrativeGenerator(use_real_llm=False)
    text = gen.generate(
        {
            "customer_id": "C1",
            "risk_score": 0.95,
            "typologies": ["Test typology"],
            "triggered_rules": ["R1"],
        }
    )
    assert "Customer C1" in text

