from xgrowth.intelligence.smart_follower_score import SmartFollowerFeatures, score_smart_follower


def test_score_is_bounded_and_explainable() -> None:
    result = score_smart_follower(
        SmartFollowerFeatures(
            relevance=1.0,
            authority=0.8,
            verification=1.0,
            recency=0.9,
            engagement_quality=0.8,
            network_value=0.7,
            conversion_likelihood=0.6,
            spam_risk=0.1,
        )
    )
    assert 0 <= result["score"] <= 100
    assert result["risk_penalty"] > 0
    assert "project heuristic" in str(result["explanation"]).lower()


def test_high_spam_risk_reduces_score() -> None:
    base = SmartFollowerFeatures(0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.0)
    risky = SmartFollowerFeatures(0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 1.0)
    assert score_smart_follower(risky)["score"] < score_smart_follower(base)["score"]
