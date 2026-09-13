from __future__ import annotations

from typing import Any


def manual_recommendations(posts: list[dict[str, Any]], limit: int = 3) -> list[dict[str, object]]:
    ranked: list[tuple[float, dict[str, Any]]] = []
    for post in posts:
        metrics = post.get("public_metrics") or {}
        impressions = max(int(metrics.get("impression_count", 0)), 0)
        replies = max(int(metrics.get("reply_count", 0)), 0)
        reposts = max(int(metrics.get("retweet_count", 0)), 0)
        quotes = max(int(metrics.get("quote_count", 0)), 0)
        meaningful_rate = (replies + reposts + quotes) / max(impressions, 1)
        ranked.append((meaningful_rate, post))

    ranked.sort(key=lambda item: item[0], reverse=True)
    output: list[dict[str, object]] = []
    for rate, post in ranked[: max(1, min(int(limit), 10))]:
        output.append(
            {
                "post_id": str(post.get("id", "")),
                "meaningful_engagement_rate": round(rate, 6),
                "recommendation": "Review this post format/topic for a similar manual follow-up.",
                "action_mode": "manual_only",
            }
        )
    return output
