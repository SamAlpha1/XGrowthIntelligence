from __future__ import annotations

from typing import Any

from xgrowth.intelligence.strategy_engine import manual_recommendations


def build_daily_report(account: dict[str, Any], posts: list[dict[str, Any]]) -> dict[str, Any]:
    public = account.get("public_metrics") or {}
    return {
        "owner": "SamAlpha1",
        "x_handle": "samalpha_",
        "account": {
            "username": str(account.get("username", "")),
            "followers": public.get("followers_count"),
            "following": public.get("following_count"),
            "posts": public.get("tweet_count"),
            "verified": account.get("verified"),
            "verified_type": account.get("verified_type"),
        },
        "recent_posts_sampled": len(posts),
        "manual_recommendations": manual_recommendations(posts),
        "safety": {"x_write_actions": 0, "action_mode": "read_only_manual_recommendations"},
    }
