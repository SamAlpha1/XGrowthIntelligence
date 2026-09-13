from datetime import datetime, timezone

import pytest

from xgrowth.intelligence.anomaly_detector import robust_drop_alert
from xgrowth.intelligence.conversion_engine import follower_growth, observed_conversion
from xgrowth.intelligence.engagement_engine import engagement_quality
from xgrowth.intelligence.follower_profile_ranker import rank_follower_profiles
from xgrowth.intelligence.impression_engine import impression_velocity
from xgrowth.intelligence.smart_follower_score import score_partial_features
from xgrowth.safety.policy_guard import PolicyViolation, assert_capability_allowed, assert_manual_recommendation


def test_partial_score_does_not_impute_missing_features() -> None:
    result = score_partial_features(
        {
            "relevance": None,
            "authority": 0.8,
            "verification": 1.0,
            "recency": None,
            "engagement_quality": None,
            "network_value": 0.7,
            "conversion_likelihood": None,
        }
    )
    assert result["evidence_coverage"] < 1
    assert "relevance" in result["missing_features"]


def test_verified_relevant_profile_ranks_above_sparse_profile() -> None:
    followers = [
        {
            "id": "1",
            "username": "strong",
            "name": "Crypto Builder",
            "description": "crypto trading python",
            "verified": True,
            "verified_type": "business",
            "public_metrics": {
                "followers_count": 50000,
                "following_count": 400,
                "tweet_count": 5000,
                "listed_count": 300,
            },
        },
        {
            "id": "2",
            "username": "sparse",
            "name": "Sparse",
            "description": "",
            "verified": False,
            "public_metrics": {
                "followers_count": 2,
                "following_count": 900,
                "tweet_count": 1,
                "listed_count": 0,
            },
        },
    ]
    ranked = rank_follower_profiles(followers, target_keywords=["crypto", "trading", "python"])
    assert ranked[0]["username"] == "strong"
    assert ranked[0]["score"] > ranked[1]["score"]


def test_engagement_and_conversion_metrics_are_bounded_by_observed_counts() -> None:
    quality = engagement_quality(
        {
            "impression_count": 1000,
            "like_count": 50,
            "reply_count": 10,
            "retweet_count": 5,
            "quote_count": 2,
        }
    )
    assert quality["engagement_rate"] == 0.067
    assert observed_conversion(20, 1000) == 0.02
    assert observed_conversion(1, 0) is None
    assert follower_growth(100, 110)["follower_delta"] == 10


def test_impression_velocity_is_age_normalized() -> None:
    now = datetime(2026, 9, 13, 12, 0, tzinfo=timezone.utc)
    assert impression_velocity(1000, "2026-09-13T10:00:00Z", now=now) == 500.0


def test_anomaly_detector_flags_material_drop() -> None:
    result = robust_drop_alert([100, 110, 90], 30, drop_ratio=0.5)
    assert result["alert"] is True


def test_policy_guard_rejects_write_capabilities_and_nonmanual_strategy() -> None:
    with pytest.raises(PolicyViolation):
        assert_capability_allowed("follow")
    with pytest.raises(PolicyViolation):
        assert_manual_recommendation("automatic")
    assert_capability_allowed("read_metrics")
    assert_manual_recommendation("manual_only")
