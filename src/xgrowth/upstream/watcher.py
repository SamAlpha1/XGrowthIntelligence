from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any

import httpx


UPSTREAM_REPO = "xai-org/x-algorithm"
TRACKED_PREFIXES = (
    "phoenix/",
    "home-mixer/",
    "vm-ranker/",
    "grox/",
    "visibility-filtering/",
    "visibility-filtering-client/",
    "user-cred-v2/",
    "under-the-hood/",
)


@dataclass(frozen=True)
class UpstreamSnapshot:
    sha: str
    committed_at: str
    message: str
    relevant_files: tuple[str, ...]
    checked_at: str

    def as_dict(self) -> dict[str, Any]:
        return {
            "repository": UPSTREAM_REPO,
            "sha": self.sha,
            "committed_at": self.committed_at,
            "message": self.message,
            "relevant_files": list(self.relevant_files),
            "checked_at": self.checked_at,
        }


def is_relevant_path(path: str) -> bool:
    return path == "home-mixer/params/param.rs" or path.startswith(TRACKED_PREFIXES)


def fetch_latest_snapshot(token: str | None = None, timeout: float = 15.0) -> UpstreamSnapshot:
    headers = {"Accept": "application/vnd.github+json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    with httpx.Client(headers=headers, timeout=timeout) as client:
        latest = client.get(f"https://api.github.com/repos/{UPSTREAM_REPO}/commits/main")
        latest.raise_for_status()
        commit = latest.json()
        sha = str(commit["sha"])
        detail = client.get(f"https://api.github.com/repos/{UPSTREAM_REPO}/commits/{sha}")
        detail.raise_for_status()
        payload = detail.json()

    files = tuple(
        sorted(
            file_info["filename"]
            for file_info in payload.get("files", [])
            if is_relevant_path(file_info.get("filename", ""))
        )
    )
    committed_at = payload.get("commit", {}).get("committer", {}).get("date", "")
    message = payload.get("commit", {}).get("message", "")
    checked_at = datetime.now(timezone.utc).isoformat()
    return UpstreamSnapshot(
        sha=sha,
        committed_at=committed_at,
        message=message,
        relevant_files=files,
        checked_at=checked_at,
    )
