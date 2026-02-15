from __future__ import annotations

import re
from urllib.parse import urlparse

URL_RE = re.compile(r"(https?://[^\s<>\"]+)", re.IGNORECASE)

SHORTENER_DOMAINS = {
    "bit.ly", "tinyurl.com", "t.co", "goo.gl", "ow.ly", "is.gd", "cutt.ly", "rb.gy"
}


def extract_urls(text: str) -> list[str]:
    if not text:
        return []
    return [m.group(1).rstrip(").,;!\"'") for m in URL_RE.finditer(text)]


def url_signals(urls: list[str]) -> dict[str, int]:
    suspicious = 0
    shorteners = 0
    ip_urls = 0
    many_params = 0

    for u in urls:
        p = urlparse(u)
        host = (p.hostname or "").lower()

        if host in SHORTENER_DOMAINS:
            shorteners += 1

        # IP in host
        if re.fullmatch(r"\d{1,3}(\.\d{1,3}){3}", host or ""):
            ip_urls += 1

        # many query params
        if p.query and p.query.count("&") >= 3:
            many_params += 1

        # very long URL
        if len(u) >= 120:
            suspicious += 1

    return {
        "url_count": len(urls),
        "shortener_count": shorteners,
        "ip_url_count": ip_urls,
        "many_params_count": many_params,
        "long_url_count": suspicious,
    }
