from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

from .intelligence.follower_profile_ranker import rank_follower_profiles
from .reporting.daily_report import build_daily_report
from .settings import Settings
from .upstream.diff_parser import classify_paths, meaningful_categories
from .upstream.watcher import fetch_latest_snapshot
from .x_api import XApiError, XReadOnlyClient


def _write_summary(markdown: str) -> None:
    target = os.getenv("GITHUB_STEP_SUMMARY", "").strip()
    if target:
        Path(target).write_text(markdown, encoding="utf-8")
    else:
        print(markdown)


def _target_keywords() -> list[str]:
    return [item.strip() for item in os.getenv("X_TARGET_KEYWORDS", "").split(",") if item.strip()]


def _bounded_env_int(name: str, default: int, minimum: int, maximum: int) -> int:
    raw = os.getenv(name, "").strip()
    if not raw:
        return default
    try:
        value = int(raw)
    except ValueError:
        return default
    return min(max(value, minimum), maximum)


def command_metrics() -> int:
    settings = Settings.from_env()
    follower_error: str | None = None
    post_sample_size = _bounded_env_int("X_POST_SAMPLE_SIZE", 5, 5, 100)
    follower_sample_size = _bounded_env_int("X_FOLLOWER_SAMPLE_SIZE", 10, 0, 1000)
    client = XReadOnlyClient(settings)
    try:
        try:
            user_payload = client.get_user_by_username(settings.x_username)
        except XApiError as exc:
            _write_summary(
                "# XGrowthIntelligence — X API blocked\n\n"
                "Owner: **SamAlpha1** · X: **@samalpha_**\n\n"
                f"Account requested: **@{settings.x_username}**\n\n"
                f"Status: **{exc}**\n\n"
                "No write action was performed.\n"
            )
            raise

        user = user_payload.get("data") or {}
        user_id = str(user.get("id", ""))
        tweets_payload = client.get_recent_tweets(user_id, max_results=post_sample_size) if user_id else {"data": []}
        followers: list[dict[str, object]] = []
        if user_id and follower_sample_size > 0:
            try:
                followers = client.get_followers_bounded(
                    user_id,
                    max_pages=1,
                    page_size=follower_sample_size,
                )
            except XApiError as exc:
                follower_error = str(exc)
    finally:
        client.close()

    posts = tweets_payload.get("data") or []
    smart_followers = rank_follower_profiles(followers, target_keywords=_target_keywords())
    report = build_daily_report(user, posts)
    snapshot = {
        "owner": "SamAlpha1",
        "x_handle": "samalpha_",
        "account": user,
        "posts": posts,
        "post_sample_limit": post_sample_size,
        "follower_sample_limit": follower_sample_size,
        "follower_sample_size": len(followers),
        "follower_ranking_error": follower_error,
        "safety": {"x_write_actions": 0, "mode": "read_only"},
    }
    smart_snapshot = {
        "owner": "SamAlpha1",
        "x_handle": "samalpha_",
        "target_keywords": _target_keywords(),
        "sample_limit": follower_sample_size,
        "sample_size": len(followers),
        "ranking_error": follower_error,
        "ranked_followers": smart_followers[:50],
        "scoring_note": "Project heuristic with explicit evidence coverage; missing features are not imputed.",
    }
    Path("metrics-snapshot.json").write_text(json.dumps(snapshot, indent=2), encoding="utf-8")
    Path("daily-report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    Path("smart-followers.json").write_text(json.dumps(smart_snapshot, indent=2), encoding="utf-8")

    metrics = user.get("public_metrics") or {}
    verified_followers = user.get("verified_followers_count", "n/a")
    follower_status = f"{len(followers)} sampled" if follower_error is None else "unavailable on current access"
    summary = (
        "# XGrowthIntelligence — Read-Only Metrics\n\n"
        "Owner: **SamAlpha1** · X: **@samalpha_**\n\n"
        f"Account checked: **@{settings.x_username}**\n\n"
        f"Followers: **{metrics.get('followers_count', 'n/a')}**  \n"
        f"Verified followers: **{verified_followers}**  \n"
        f"Following: **{metrics.get('following_count', 'n/a')}**  \n"
        f"Posts: **{metrics.get('tweet_count', 'n/a')}**  \n"
        f"Recent original posts sampled: **{len(posts)}** / limit {post_sample_size}  \n"
        f"Follower ranking input: **{follower_status}** / limit {follower_sample_size}\n\n"
        "Recommendations are manual-only. No write action was performed.\n"
    )
    _write_summary(summary)
    return 0


def command_upstream() -> int:
    snapshot = fetch_latest_snapshot(token=os.getenv("GITHUB_TOKEN"))
    meaningful_paths = [
        str(item["source_path"])
        for item in snapshot.change_evidence
        if item.get("meaningful") is True
    ]
    ignored_paths = [
        str(item["source_path"])
        for item in snapshot.change_evidence
        if item.get("meaningful") is False
    ]
    uncertain_paths = [
        str(item["source_path"])
        for item in snapshot.change_evidence
        if item.get("meaningful") is None
    ]
    signals = classify_paths(meaningful_paths)
    categories = meaningful_categories(signals)
    payload = snapshot.as_dict() | {
        "meaningful_categories": list(categories),
        "meaningful_paths": meaningful_paths,
        "ignored_nonsemantic_paths": ignored_paths,
        "uncertain_paths": uncertain_paths,
    }
    Path("upstream-snapshot.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")
    meaningful_text = "\n".join(f"- `{path}`" for path in meaningful_paths) or "- none"
    ignored_text = "\n".join(f"- `{path}`" for path in ignored_paths) or "- none"
    uncertain_text = "\n".join(f"- `{path}`" for path in uncertain_paths) or "- none"
    categories_text = ", ".join(categories) if categories else "none"
    _write_summary(
        "# XGrowthIntelligence — Upstream Watch\n\n"
        "Owner: **SamAlpha1** · X: **@samalpha_**\n\n"
        f"Commit: `{snapshot.sha}`  \n"
        f"Committed: `{snapshot.committed_at}`  \n"
        f"Meaningful source categories: **{categories_text}**\n\n"
        "## Meaningful source changes\n"
        f"{meaningful_text}\n\n"
        "## Ignored metadata/comment-only changes\n"
        f"{ignored_text}\n\n"
        "## Patch unavailable / uncertain\n"
        f"{uncertain_text}\n\n"
        "No ranking effect or weight is inferred automatically from a source change.\n"
    )
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="xgrowth")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("metrics")
    sub.add_parser("upstream")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    if args.command == "metrics":
        return command_metrics()
    if args.command == "upstream":
        return command_upstream()
    raise RuntimeError("Unsupported command")


if __name__ == "__main__":
    raise SystemExit(main())
