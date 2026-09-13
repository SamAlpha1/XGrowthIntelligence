from __future__ import annotations

from dataclasses import asdict
from typing import Any

from .diff_parser import classify_paths


def extract_path_evidence(sha: str, paths: list[str], extracted_at: str) -> dict[str, Any]:
    signals = classify_paths(paths)
    return {
        "commit_sha": sha,
        "extracted_at": extracted_at,
        "evidence_type": "changed-path classification",
        "signals": [asdict(signal) for signal in signals],
        "notes": "No ranking weight is inferred from a changed path alone.",
    }
