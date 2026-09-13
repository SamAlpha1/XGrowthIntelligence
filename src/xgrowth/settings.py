from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    x_username: str
    x_bearer_token: str
    request_timeout_seconds: float = 15.0
    max_retries: int = 2

    @classmethod
    def from_env(cls) -> "Settings":
        username = os.getenv("X_USERNAME", "").strip().lstrip("@")
        token = os.getenv("X_BEARER_TOKEN", "").strip()
        if not username:
            raise RuntimeError("X_USERNAME is required")
        if not token:
            raise RuntimeError("X_BEARER_TOKEN is required")
        return cls(x_username=username, x_bearer_token=token)
