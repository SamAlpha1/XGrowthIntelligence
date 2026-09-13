from __future__ import annotations


def follower_growth(previous_followers: int, current_followers: int) -> dict[str, float | int]:
    previous = max(int(previous_followers), 0)
    current = max(int(current_followers), 0)
    delta = current - previous
    rate = delta / max(previous, 1)
    return {
        "previous_followers": previous,
        "current_followers": current,
        "follower_delta": delta,
        "follower_growth_rate": round(rate, 6),
    }


def observed_conversion(numerator: int, denominator: int) -> float | None:
    top = max(int(numerator), 0)
    bottom = max(int(denominator), 0)
    if bottom == 0:
        return None
    return round(top / bottom, 6)
