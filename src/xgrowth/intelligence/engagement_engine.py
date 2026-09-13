from __future__ import annotations


def engagement_quality(public_metrics: dict[str, int]) -> dict[str, float]:
    impressions = max(int(public_metrics.get("impression_count", 0)), 0)
    likes = max(int(public_metrics.get("like_count", 0)), 0)
    replies = max(int(public_metrics.get("reply_count", 0)), 0)
    reposts = max(int(public_metrics.get("retweet_count", 0)), 0)
    quotes = max(int(public_metrics.get("quote_count", 0)), 0)
    denominator = max(impressions, 1)
    meaningful = replies + reposts + quotes
    return {
        "engagement_rate": round((likes + meaningful) / denominator, 6),
        "meaningful_engagement_rate": round(meaningful / denominator, 6),
        "reply_rate": round(replies / denominator, 6),
        "share_rate": round((reposts + quotes) / denominator, 6),
    }
