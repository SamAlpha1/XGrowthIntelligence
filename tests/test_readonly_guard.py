import pytest

from xgrowth.safety.readonly_guard import ReadOnlyViolation, assert_no_write_scope, enforce_readonly


def test_get_is_allowed() -> None:
    enforce_readonly("GET", "https://api.x.com/2/users/by/username/samalpha_")


@pytest.mark.parametrize("method", ["POST", "PUT", "PATCH", "DELETE"])
def test_write_methods_are_blocked(method: str) -> None:
    with pytest.raises(ReadOnlyViolation):
        enforce_readonly(method, "https://api.x.com/2/tweets")


def test_unexpected_host_is_blocked() -> None:
    with pytest.raises(ReadOnlyViolation):
        enforce_readonly("GET", "https://example.com/2/users/me")


def test_write_scopes_are_blocked() -> None:
    with pytest.raises(ReadOnlyViolation):
        assert_no_write_scope("users.read tweet.read tweet.write")


def test_read_scopes_are_allowed() -> None:
    assert_no_write_scope("users.read tweet.read")
