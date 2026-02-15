from __future__ import annotations

from typing import Any


def score(signals: dict[str, Any]) -> tuple[int, list[str]]:
    points = 0
    reasons: list[str] = []

    # URLs
    if signals.get("url_count", 0) >= 3:
        points += 10; reasons.append("Many links in body")
    if signals.get("shortener_count", 0) > 0:
        points += 20; reasons.append("URL shortener used")
    if signals.get("ip_url_count", 0) > 0:
        points += 25; reasons.append("Link uses an IP address instead of a domain")
    if signals.get("many_params_count", 0) > 0:
        points += 10; reasons.append("Links contain many tracking/query parameters")
    if signals.get("long_url_count", 0) > 0:
        points += 5; reasons.append("Very long link(s)")

    # Headers/metadata
    if signals.get("reply_to_mismatch", 0) == 1:
        points += 15; reasons.append("Reply-To domain differs from From domain")
    if signals.get("urgent_subject", 0) == 1:
        points += 10; reasons.append("Urgency/pressure language in subject")
    if signals.get("has_auth_results", 0) == 0:
        points += 10; reasons.append("Missing common authentication-related headers")

    # Clamp
    points = max(0, min(100, points))
    return points, reasons
