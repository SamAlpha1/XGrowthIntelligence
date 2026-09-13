from __future__ import annotations

from dataclasses import dataclass

from .smart_follower_score import SmartFollowerFeatures, score_smart_follower


@dataclass(frozen=True)
class AccountCandidate:
    username: str
    relevance: float
    authority: float
    verification: float
    recency: float
    engagement_quality: float
    network_value: float
    conversion_likelihood: float
    spam_risk: float = 0.0


def rank_accounts(candidates: list[AccountCandidate]) -> list[dict[str, object]]:
    ranked: list[dict[str, object]] = []
    for candidate in candidates:
        result = score_smart_follower(
            SmartFollowerFeatures(
                relevance=candidate.relevance,
                authority=candidate.authority,
                verification=candidate.verification,
                recency=candidate.recency,
                engagement_quality=candidate.engagement_quality,
                network_value=candidate.network_value,
                conversion_likelihood=candidate.conversion_likelihood,
                spam_risk=candidate.spam_risk,
            )
        )
        ranked.append({"username": candidate.username.lstrip("@"), **result})
    return sorted(ranked, key=lambda item: float(item["score"]), reverse=True)
