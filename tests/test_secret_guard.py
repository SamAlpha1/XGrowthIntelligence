from xgrowth.safety.secret_guard import contains_probable_secret, redact


def test_bearer_token_is_redacted() -> None:
    text = "Authorization: Bearer abcDEF123.secret"
    assert "abcDEF123" not in redact(text)


def test_assignment_is_detected() -> None:
    assert contains_probable_secret("X_BEARER_TOKEN=real-looking-token")


def test_safe_text_is_not_flagged() -> None:
    assert not contains_probable_secret("X_BEARER_TOKEN=${{ secrets.X_BEARER_TOKEN }}")
