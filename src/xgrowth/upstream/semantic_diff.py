from __future__ import annotations

import re


_DIFF_HEADER_PREFIXES = ("+++", "---", "@@")
_SYNC_MARKER = re.compile(r"last\s+sync\s+\d{4}-\d{2}-\d{2}T", re.IGNORECASE)


def _changed_lines(patch: str) -> list[str]:
    lines: list[str] = []
    for line in patch.splitlines():
        if line.startswith(_DIFF_HEADER_PREFIXES):
            continue
        if line.startswith(("+", "-")):
            lines.append(line[1:].strip())
    return lines


def classify_patch(path: str, patch: str | None) -> dict[str, object]:
    if patch is None:
        return {
            "classification": "patch_unavailable",
            "meaningful": None,
            "evidence_level": "insufficient",
            "reason": "GitHub did not provide a textual patch for this file.",
        }

    changed = [line for line in _changed_lines(patch) if line]
    if not changed:
        return {
            "classification": "no_changed_text",
            "meaningful": False,
            "evidence_level": "high",
            "reason": "No added or removed textual lines were present.",
        }

    if path == "home-mixer/params/param.rs" and all(_SYNC_MARKER.search(line) for line in changed):
        return {
            "classification": "sync_metadata_only",
            "meaningful": False,
            "evidence_level": "high",
            "reason": "Only the mirrored configuration sync timestamp changed.",
        }

    non_comment = [
        line
        for line in changed
        if not line.startswith(("//", "#", "/*", "*", "*/"))
    ]
    if not non_comment:
        return {
            "classification": "comment_only",
            "meaningful": False,
            "evidence_level": "high",
            "reason": "Only comments changed; no executable/source declaration change detected.",
        }

    return {
        "classification": "source_change",
        "meaningful": True,
        "evidence_level": "path_and_patch",
        "reason": "At least one non-comment source line changed; no ranking effect is inferred automatically.",
    }
