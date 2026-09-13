from __future__ import annotations

import math
from typing import Any

from .smart_follower_score import score_partial_features


def _keyword_relevance(user: dict[str, Any], target_keywords: list[str]) -> float | None:
    keywords = [item.strip().lower() for item in target_keywords if item.strip()]
    if not keywords:
        return None
    haystack = " ".join(
        str(user.get(key, "")) for key in ("name", "username", "description")
    ).lower()
    matches = sum(1 for keyword in keywords if keyword in haystack)
    return min(matches / max(len(keywords), 1), 1.0)


def _authority(public_metrics: dict[str, Any]) -> float:
    followers = max(int(public_metrics.get("followers_count", 0)), 0)
    listed = max(int(public_metrics.get("listed_count", 0)), 0)
    follower_component = min(math.log10(followers + 1) / 6.0, 1.0)
    listed_component = min(math.log10(listed + 1) / 4.0, 1.0)
    return 0.8 * follower_component + 0.2 * listed_component


def _verification(user: dict[str, Any]) -> float:
    if not bool(user.get("verified")):
        return 0.0
    verified_type = str(user.get("verified_type") or "").lower()
    if verified_type in {"business", "government"}:
        return 1.0
    return 0.75


def _network_value(public_metrics: dict[str, Any]) -> float:
    followers = max(int(public_metrics.get("followers_count", 0)), 0)
    following = max(int(public_metrics.get("following_count", 0)), 0)
    ratio = followers / max(following, 1)
    return ratio / (ratio + 1.0)


def _spam_risk(public_metrics: dict[str, Any]) -> float:
    followers = max(int(public_metrics.get("followers_count", 0)), 0)
    following = max(int(public_metrics.get("following_count", 0)), 0)
    posts = max(int(public_metrics.get("tweet_count", 0)), 0)
    risk = 0.0
    if following >= 500 and following > max(followers, 1) * 10:
        risk += 0.45
    if posts < 5:
        risk += 0.25
    if followers == 0 and following > 100:
        risk += 0.25
    return min(risk, 1.0)


def rank_follower_profiles(
    followers: list[dict[str, Any]],
    target_keywords: list[str] | None = None,
) -> list[dict[str, object]]:
    keywords = target_keywords or []
    ranked: list[dict[str, object]] = []
    for user in followers:
        public_metrics = user.get("public_metrics") or {}
        features = {
            "relevance": _keyword_relevance(user, keywords),
            "authority": _authority(public_metrics),
            "verification": _verification(user),
            "recency": None,
            "engagement_quality": None,
            "network_value": _network_value(public_metrics),
            "conversion_likelihood": None,
        }
        score = score_partial_features(features, spam_risk=_spam_risk(public_metrics))
        ranked.append(
            {
                "id": str(user.get("id", "")),
                "username": str(user.get("username", "")),
                "name": str(user.get("name", "")),
                "verified": bool(user.get("verified")),
                "verified_type": user.get("verified_type"),
                "followers_count": int(public_metrics.get("followers_count", 0) or 0),
                "following_count": int(public_metrics.get("following_count", 0) or 0),
                "tweet_count": int(public_metrics.get("tweet_count", 0) or 0),
                **score,
            }
        )
    return sorted(ranked, key=lambda item: float(item["score"]), reverse=True)
