from __future__ import annotations

import re

AUTH_HEADER_KEYS = ("Authentication-Results", "Received-SPF", "DKIM-Signature")


def header_signals(headers: dict[str, str]) -> dict[str, int]:
    has_auth_results = 1 if any(k in headers for k in AUTH_HEADER_KEYS) else 0

    reply_to = headers.get("Reply-To", "")
    from_ = headers.get("From", "")

    # crude mismatch heuristic (defensive; not a verdict)
    mismatch = 0
    if reply_to and from_:
        from_domain = _extract_domain(from_)
        reply_domain = _extract_domain(reply_to)
        if from_domain and reply_domain and from_domain != reply_domain:
            mismatch = 1

    subject = headers.get("Subject", "")
    urgent = 1 if re.search(r"\b(urgent|immediately|action required|verify|suspended)\b", subject, re.I) else 0

    return {
        "has_auth_results": has_auth_results,
        "reply_to_mismatch": mismatch,
        "urgent_subject": urgent,
    }


def _extract_domain(addr_field: str) -> str:
    m = re.search(r"@([A-Za-z0-9\.\-]+\.[A-Za-z]{2,})", addr_field)
    return (m.group(1).lower() if m else "")
