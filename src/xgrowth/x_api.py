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
    USER_FIELDS = (
        "created_at,description,public_metrics,verified,verified_type,"
        "verified_followers_count,subscription_type,affiliation"
    )

    def __init__(self, settings: Settings, transport: httpx.BaseTransport | None = None) -> None:
        self.settings = settings
        self._client = httpx.Client(
            headers={"Authorization": f"Bearer {settings.x_bearer_token}"},
            timeout=settings.request_timeout_seconds,
            transport=transport,
        )

    def close(self) -> None:
        self._client.close()

    @staticmethod
    def _client_error_message(status_code: int) -> str:
        messages = {
            400: "X API rejected the read-only request as invalid",
            401: "X API authentication failed; verify the Bearer Token",
            402: "X API credits are required; add prepaid credits in the X Developer Console",
            403: "X API denied access to this read-only endpoint for the current app",
            404: "X API resource was not found",
        }
        return messages.get(status_code, f"X API returned non-retriable HTTP {status_code}")

    def _get(self, path: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        url = f"{self.BASE_URL}{path}"
        enforce_readonly("GET", url)
        attempts = self.settings.max_retries + 1
        last_error: Exception | None = None

        for attempt in range(attempts):
            try:
                response = self._client.get(url, params=params)
            except httpx.HTTPError as exc:
                last_error = exc
                if attempt + 1 >= attempts:
                    break
                time.sleep(min(0.5 * (attempt + 1), 1.5))
                continue

            if response.status_code == 429:
                if attempt + 1 >= attempts:
                    raise XApiError("X API rate limit reached after bounded retries")
                retry_after = min(float(response.headers.get("retry-after", "1")), 5.0)
                time.sleep(max(retry_after, 0.0))
                continue

            if 400 <= response.status_code < 500:
                raise XApiError(self._client_error_message(response.status_code))

            try:
                response.raise_for_status()
                payload = response.json()
            except (httpx.HTTPError, ValueError) as exc:
                last_error = exc
                if attempt + 1 >= attempts:
                    break
                time.sleep(min(0.5 * (attempt + 1), 1.5))
                continue

            if not isinstance(payload, dict):
                raise XApiError("Unexpected X API response shape")
            return payload

        raise XApiError(f"Read-only request failed after {attempts} attempts") from last_error

    def get_user_by_username(self, username: str) -> dict[str, Any]:
        clean = username.strip().lstrip("@")
        return self._get(
            f"/users/by/username/{clean}",
            params={"user.fields": self.USER_FIELDS},
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

    def get_followers_page(
        self,
        user_id: str,
        max_results: int = 100,
        pagination_token: str | None = None,
    ) -> dict[str, Any]:
        bounded = min(max(int(max_results), 1), 1000)
        params: dict[str, Any] = {
            "max_results": bounded,
            "user.fields": self.USER_FIELDS,
        }
        if pagination_token:
            params["pagination_token"] = pagination_token
        return self._get(f"/users/{user_id}/followers", params=params)

    def get_followers_bounded(
        self,
        user_id: str,
        max_pages: int = 2,
        page_size: int = 100,
    ) -> list[dict[str, Any]]:
        pages = min(max(int(max_pages), 1), 5)
        followers: list[dict[str, Any]] = []
        token: str | None = None
        for _ in range(pages):
            payload = self.get_followers_page(user_id, max_results=page_size, pagination_token=token)
            data = payload.get("data") or []
            if isinstance(data, list):
                followers.extend(item for item in data if isinstance(item, dict))
            meta = payload.get("meta") or {}
            next_token = meta.get("next_token")
            if not next_token:
                break
            token = str(next_token)
        return followers
