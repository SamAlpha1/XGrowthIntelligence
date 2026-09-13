from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class DiffSignal:
    category: str
    source_path: str
    evidence_level: str
    reason: str


def classify_paths(paths: Iterable[str]) -> list[DiffSignal]:
    signals: list[DiffSignal] = []
    for path in sorted(set(paths)):
        if path.startswith("phoenix/"):
            signals.append(DiffSignal("phoenix", path, "path-evidence", "Phoenix source changed"))
        elif path.startswith("home-mixer/"):
            signals.append(DiffSignal("home-mixer", path, "path-evidence", "Home Mixer source changed"))
        elif path.startswith("vm-ranker/"):
            signals.append(DiffSignal("vm-ranker", path, "path-evidence", "VMRanker source changed"))
        elif path.startswith("grox/"):
            signals.append(DiffSignal("content-understanding", path, "path-evidence", "Content-understanding source changed"))
        elif path.startswith("visibility-filtering"):
            signals.append(DiffSignal("visibility", path, "path-evidence", "Visibility source changed"))
        elif path.startswith("user-cred-v2/"):
            signals.append(DiffSignal("user-cred", path, "path-evidence", "User credibility source changed"))
        elif path.startswith("under-the-hood/"):
            signals.append(DiffSignal("under-the-hood", path, "path-evidence", "Public reporting source changed"))
    return signals


def meaningful_categories(signals: Iterable[DiffSignal]) -> tuple[str, ...]:
    return tuple(sorted({signal.category for signal in signals}))
