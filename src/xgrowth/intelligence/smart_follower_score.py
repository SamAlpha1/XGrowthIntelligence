from __future__ import annotations

from dataclasses import dataclass


def _bounded(value: float) -> float:
    return max(0.0, min(float(value), 1.0))


@dataclass(frozen=True)
class SmartFollowerFeatures:
    relevance: float
    authority: float
    verification: float
    recency: float
    engagement_quality: float
    network_value: float
    conversion_likelihood: float
    spam_risk: float = 0.0


DEFAULT_WEIGHTS = {
    "relevance": 0.24,
    "authority": 0.16,
    "verification": 0.12,
    "recency": 0.12,
    "engagement_quality": 0.16,
    "network_value": 0.10,
    "conversion_likelihood": 0.10,
}


def score_smart_follower(
    features: SmartFollowerFeatures,
    weights: dict[str, float] | None = None,
    risk_penalty_max: float = 0.35,
) -> dict[str, object]:
    active = weights or DEFAULT_WEIGHTS
    values = {
        "relevance": _bounded(features.relevance),
        "authority": _bounded(features.authority),
        "verification": _bounded(features.verification),
        "recency": _bounded(features.recency),
        "engagement_quality": _bounded(features.engagement_quality),
        "network_value": _bounded(features.network_value),
        "conversion_likelihood": _bounded(features.conversion_likelihood),
    }
    weighted_parts = {name: values[name] * active[name] for name in active}
    raw = sum(weighted_parts.values())
    penalty = _bounded(features.spam_risk) * max(0.0, min(risk_penalty_max, 1.0))
    final = max(0.0, min(raw - penalty, 1.0))
    return {
        "score": round(final * 100, 2),
        "raw_score": round(raw * 100, 2),
        "risk_penalty": round(penalty * 100, 2),
        "components": {key: round(value * 100, 2) for key, value in weighted_parts.items()},
        "evidence_coverage": 1.0,
        "explanation": "Internal project heuristic; not an upstream X ranking weight.",
    }


def score_partial_features(
    features: dict[str, float | None],
    spam_risk: float = 0.0,
    weights: dict[str, float] | None = None,
    risk_penalty_max: float = 0.35,
) -> dict[str, object]:
    active = weights or DEFAULT_WEIGHTS
    available = {
        name: _bounded(value)
        for name, value in features.items()
        if name in active and value is not None
    }
    available_weight = sum(active[name] for name in available)
    total_weight = sum(active.values())
    if available_weight <= 0:
        return {
            "score": 0.0,
            "raw_score": 0.0,
            "risk_penalty": 0.0,
            "components": {},
            "evidence_coverage": 0.0,
            "missing_features": sorted(active),
            "explanation": "Insufficient evidence for a project heuristic score.",
        }

    parts = {name: available[name] * active[name] for name in available}
    normalized_raw = sum(parts.values()) / available_weight
    penalty = _bounded(spam_risk) * max(0.0, min(risk_penalty_max, 1.0))
    final = max(0.0, min(normalized_raw - penalty, 1.0))
    return {
        "score": round(final * 100, 2),
        "raw_score": round(normalized_raw * 100, 2),
        "risk_penalty": round(penalty * 100, 2),
        "components": {key: round(value * 100, 2) for key, value in parts.items()},
        "evidence_coverage": round(available_weight / max(total_weight, 1e-9), 4),
        "missing_features": sorted(set(active) - set(available)),
        "explanation": "Evidence-normalized project heuristic; missing features are not imputed.",
    }
