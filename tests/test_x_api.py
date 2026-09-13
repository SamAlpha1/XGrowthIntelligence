import httpx

from xgrowth.settings import Settings
from xgrowth.x_api import XReadOnlyClient


def test_user_lookup_is_get_only() -> None:
    seen = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append((request.method, str(request.url)))
        return httpx.Response(
            200,
            json={"data": {"id": "1", "username": "samalpha_"}},
        )

    settings = Settings(x_username="samalpha_", x_bearer_token="test-token", max_retries=0)
    client = XReadOnlyClient(settings, transport=httpx.MockTransport(handler))
    try:
        payload = client.get_user_by_username("@samalpha_")
    finally:
        client.close()

    assert payload["data"]["username"] == "samalpha_"
    assert seen and seen[0][0] == "GET"
    assert "/users/by/username/samalpha_" in seen[0][1]
