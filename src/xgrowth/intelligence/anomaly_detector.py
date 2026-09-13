from __future__ import annotations

from statistics import median


def robust_drop_alert(history: list[float], current: float, drop_ratio: float = 0.5) -> dict[str, object]:
    clean = [max(float(value), 0.0) for value in history]
    current_value = max(float(current), 0.0)
    if not clean:
        return {"alert": False, "baseline": None, "current": current_value, "reason": "no_history"}
    baseline = median(clean)
    threshold = baseline * max(0.0, min(float(drop_ratio), 1.0))
    alert = baseline > 0 and current_value < threshold
    return {
        "alert": alert,
        "baseline": round(baseline, 6),
        "current": round(current_value, 6),
        "reason": "material_drop" if alert else "within_baseline",
    }
