from __future__ import annotations


class PolicyViolation(RuntimeError):
    pass


_FORBIDDEN_CAPABILITIES = {
    "post",
    "delete_post",
    "follow",
    "unfollow",
    "like",
    "unlike",
    "reply",
    "quote",
    "repost",
    "unrepost",
    "dm",
    "upload_media",
}


def assert_capability_allowed(capability: str) -> None:
    normalized = capability.strip().lower()
    if normalized in _FORBIDDEN_CAPABILITIES:
        raise PolicyViolation(f"Forbidden v1 X capability: {normalized}")


def assert_manual_recommendation(action_mode: str) -> None:
    if action_mode.strip().lower() != "manual_only":
        raise PolicyViolation("Strategy recommendations must remain manual-only in v1")
