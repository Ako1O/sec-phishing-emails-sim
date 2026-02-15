from __future__ import annotations

from dataclasses import dataclass
from email import policy
from email.parser import BytesParser
from pathlib import Path
from typing import Optional


@dataclass(frozen=True)
class ParsedEmail:
    subject: str
    from_: str
    to: str
    reply_to: str
    date: str
    headers: dict[str, str]
    body_text: str
    body_html: str


def _get_first(payload_list: list[Optional[str]]) -> str:
    for x in payload_list:
        if x:
            return x
    return ""


def parse_eml(path: Path) -> ParsedEmail:
    raw = path.read_bytes()
    msg = BytesParser(policy=policy.default).parsebytes(raw)

    headers = {k: str(v) for (k, v) in msg.items()}

    subject = str(msg.get("Subject", ""))
    from_ = str(msg.get("From", ""))
    to = str(msg.get("To", ""))
    reply_to = str(msg.get("Reply-To", ""))
    date = str(msg.get("Date", ""))

    body_text_parts: list[Optional[str]] = []
    body_html_parts: list[Optional[str]] = []

    if msg.is_multipart():
        for part in msg.walk():
            ctype = part.get_content_type()
            disp = str(part.get("Content-Disposition", ""))
            if "attachment" in disp.lower():
                continue
            if ctype == "text/plain":
                body_text_parts.append(part.get_content())
            elif ctype == "text/html":
                body_html_parts.append(part.get_content())
    else:
        ctype = msg.get_content_type()
        if ctype == "text/plain":
            body_text_parts.append(msg.get_content())
        elif ctype == "text/html":
            body_html_parts.append(msg.get_content())

    return ParsedEmail(
        subject=subject,
        from_=from_,
        to=to,
        reply_to=reply_to,
        date=date,
        headers=headers,
        body_text=_get_first(body_text_parts),
        body_html=_get_first(body_html_parts),
    )
