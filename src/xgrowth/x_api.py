from __future__ import annotations

import time
from typing import Any

import httpx

from .safety.readonly_guard import enforce_readonly
from .settings import Settings


class XApiError(RuntimeError):
    pass


class XReadOnlyClient:
    BASE_URL = "https://api.x.com/2"

    def __init__(self, settings: Settings, transport: httpx.BaseTransport | None = None) -> None:
        self.settings = settings
        self._client = httpx.Client(
            headers={"Authorization": f"Bearer {settings.x_bearer_token}"},
            timeout=settings.request_timeout_seconds,
            transport=transport,
        )

    def close(self) -> None:
        self._client.close()

    def _get(self, path: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        url = f"{self.BASE_URL}{path}"
        enforce_readonly("GET", url)
        attempts = self.settings.max_retries + 1
        last_error: Exception | None = None

        for attempt in range(attempts):
            try:
                response = self._client.get(url, params=params)
                if response.status_code == 429:
                    if attempt + 1 >= attempts:
                        raise XApiError("X API rate limit reached after bounded retries")
                    retry_after = min(float(response.headers.get("retry-after", "1")), 5.0)
                    time.sleep(max(retry_after, 0.0))
                    continue
                response.raise_for_status()
                payload = response.json()
                if not isinstance(payload, dict):
                    raise XApiError("Unexpected X API response shape")
                return payload
            except (httpx.HTTPError, ValueError, XApiError) as exc:
                last_error = exc
                if attempt + 1 >= attempts:
                    break
                time.sleep(min(0.5 * (attempt + 1), 1.5))

        raise XApiError(f"Read-only request failed after {attempts} attempts") from last_error

    def get_user_by_username(self, username: str) -> dict[str, Any]:
        clean = username.strip().lstrip("@")
        return self._get(
            f"/users/by/username/{clean}",
            params={
                "user.fields": "created_at,description,public_metrics,verified,verified_type",
            },
        )

    def get_recent_tweets(self, user_id: str, max_results: int = 10) -> dict[str, Any]:
        bounded = min(max(max_results, 5), 100)
        return self._get(
            f"/users/{user_id}/tweets",
            params={
                "max_results": bounded,
                "exclude": "retweets,replies",
                "tweet.fields": "created_at,public_metrics,possibly_sensitive",
            },
        )
