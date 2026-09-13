from __future__ import annotations

from typing import Any


def render_daily_summary(report: dict[str, Any]) -> str:
    account = report.get("account") or {}
    recommendations = report.get("manual_recommendations") or []
    lines = [
        "# XGrowthIntelligence — Daily Report",
        "",
        "Owner: **SamAlpha1** · X: **@samalpha_**",
        "",
        f"Account: **@{account.get('username', '')}**",
        f"Followers: **{account.get('followers', 'n/a')}**",
        f"Recent posts sampled: **{report.get('recent_posts_sampled', 0)}**",
        "",
        "## Manual review candidates",
    ]
    if recommendations:
        for item in recommendations:
            lines.append(
                f"- Post `{item.get('post_id', '')}` — meaningful engagement rate "
                f"`{item.get('meaningful_engagement_rate', 0)}`"
            )
    else:
        lines.append("- No recommendation evidence available in this sample.")
    lines.extend(["", "Read-only analysis only. No X write action was performed."])
    return "\n".join(lines) + "\n"
