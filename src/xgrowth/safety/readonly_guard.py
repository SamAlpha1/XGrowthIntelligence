from __future__ import annotations

from urllib.parse import urlparse


class ReadOnlyViolation(RuntimeError):
    pass


_ALLOWED_METHODS = {"GET", "HEAD"}
_ALLOWED_HOSTS = {"api.x.com", "api.twitter.com"}


def enforce_readonly(method: str, url: str) -> None:
    normalized_method = method.upper().strip()
    if normalized_method not in _ALLOWED_METHODS:
        raise ReadOnlyViolation(f"Blocked non-read method: {normalized_method}")

    parsed = urlparse(url)
    host = (parsed.hostname or "").lower()
    if host not in _ALLOWED_HOSTS:
        raise ReadOnlyViolation(f"Blocked unexpected X API host: {host or '<missing>'}")


def assert_no_write_scope(scope_text: str) -> None:
    forbidden = {
        "tweet.write",
        "users.write",
        "like.write",
        "follows.write",
        "dm.write",
        "offline.access",
    }
    scopes = {part.strip().lower() for part in scope_text.replace(",", " ").split() if part.strip()}
    overlap = forbidden.intersection(scopes)
    if overlap:
        raise ReadOnlyViolation(f"Write-capable scopes are forbidden in v1: {sorted(overlap)}")
