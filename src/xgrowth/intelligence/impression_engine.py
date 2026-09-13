from __future__ import annotations

from datetime import datetime, timezone


def impression_velocity(impressions: int, created_at: str, now: datetime | None = None) -> float:
    reference = now or datetime.now(timezone.utc)
    created = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
    age_seconds = max((reference - created).total_seconds(), 60.0)
    age_hours = age_seconds / 3600.0
    return round(max(int(impressions), 0) / age_hours, 4)


def age_normalized_impressions(impressions: int, age_hours: float) -> float:
    bounded_age = max(float(age_hours), 1.0 / 60.0)
    return round(max(int(impressions), 0) / bounded_age, 4)
