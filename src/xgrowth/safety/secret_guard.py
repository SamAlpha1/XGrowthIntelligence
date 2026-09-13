from __future__ import annotations

import re


_SECRET_PATTERNS = [
    re.compile(r"(?i)bearer\s+[A-Za-z0-9._~+\-/]+=*"),
    re.compile(r"(?i)X_BEARER_TOKEN\s*=\s*[^\s$][^\s]*"),
]


def redact(text: str) -> str:
    redacted = text
    for pattern in _SECRET_PATTERNS:
        redacted = pattern.sub("[REDACTED]", redacted)
    return redacted


def contains_probable_secret(text: str) -> bool:
    return any(pattern.search(text) for pattern in _SECRET_PATTERNS)
