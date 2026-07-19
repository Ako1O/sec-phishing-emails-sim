from __future__ import annotations

from pathlib import Path

from phishing_sim.analyzer.parse_eml import parse_eml
from phishing_sim.analyzer.url_features import extract_urls, url_signals
from phishing_sim.analyzer.header_features import header_signals
from phishing_sim.analyzer.scoring import score


def analyze_eml_to_report(path: Path) -> dict:
    eml = parse_eml(path)
    combined_text = "\n".join([eml.subject, eml.body_text, eml.body_html])

    urls = sorted(set(extract_urls(combined_text)))
    u = url_signals(urls)
    h = header_signals(eml.headers)

    signals = {**u, **h}
    s, reasons = score(signals)

    level = "LOW"
    if s >= 70:
        level = "HIGH"
    elif s >= 40:
        level = "MEDIUM"

    return {
        "file": path.as_posix(),
        "score": s,
        "level": level,
        "top_reasons": reasons,
        "signals": signals,
        "urls": urls,
        "from": eml.from_,
        "to": eml.to,
        "subject": eml.subject,
        "date": eml.date,
    }
