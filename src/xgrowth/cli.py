from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

from .settings import Settings
from .upstream.diff_parser import classify_paths, meaningful_categories
from .upstream.watcher import fetch_latest_snapshot
from .x_api import XReadOnlyClient


def _write_summary(markdown: str) -> None:
    target = os.getenv("GITHUB_STEP_SUMMARY", "").strip()
    if target:
        Path(target).write_text(markdown, encoding="utf-8")
    else:
        print(markdown)


def command_metrics() -> int:
    settings = Settings.from_env()
    client = XReadOnlyClient(settings)
    try:
        user_payload = client.get_user_by_username(settings.x_username)
        user = user_payload.get("data") or {}
        user_id = str(user.get("id", ""))
        tweets_payload = client.get_recent_tweets(user_id, max_results=10) if user_id else {"data": []}
    finally:
        client.close()

    metrics = user.get("public_metrics") or {}
    tweet_count = len(tweets_payload.get("data") or [])
    summary = (
        "# XGrowthIntelligence — Read-Only Metrics\n\n"
        f"Owner: **SamAlpha1** · X: **@samalpha_**\n\n"
        f"Account checked: **@{settings.x_username}**\n\n"
        f"Followers: **{metrics.get('followers_count', 'n/a')}**  \n"
        f"Following: **{metrics.get('following_count', 'n/a')}**  \n"
        f"Posts: **{metrics.get('tweet_count', 'n/a')}**  \n"
        f"Recent original posts sampled: **{tweet_count}**\n\n"
        "No write action was performed.\n"
    )
    _write_summary(summary)
    return 0


def command_upstream() -> int:
    snapshot = fetch_latest_snapshot(token=os.getenv("GITHUB_TOKEN"))
    signals = classify_paths(snapshot.relevant_files)
    categories = meaningful_categories(signals)
    payload = snapshot.as_dict() | {"meaningful_categories": list(categories)}
    Path("upstream-snapshot.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")
    files = "\n".join(f"- `{path}`" for path in snapshot.relevant_files) or "- No tracked paths changed"
    categories_text = ", ".join(categories) if categories else "none"
    _write_summary(
        "# XGrowthIntelligence — Upstream Watch\n\n"
        f"Owner: **SamAlpha1** · X: **@samalpha_**\n\n"
        f"Commit: `{snapshot.sha}`  \n"
        f"Committed: `{snapshot.committed_at}`  \n"
        f"Tracked categories: **{categories_text}**\n\n"
        f"{files}\n\n"
        "Changed paths are evidence of code movement only; no ranking weight is inferred automatically.\n"
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
