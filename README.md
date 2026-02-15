# sec-phishing-emails-sim

Defensive phishing email analysis toolkit written in Python.

This project analyzes `.eml` email files and produces a structured risk report based on URL signals, header anomalies, and heuristic scoring.

This tool is strictly defensive. It does **not** generate phishing emails.

---

## WORK IN PROGRESS !!!

##  Features

- Parse `.eml` email files
- Extract URLs from body (text + HTML)
- Detect:
  - URL shorteners
  - IP-based links
  - Excessive query parameters
  - Suspicious subject language
  - Reply-To domain mismatches
  - Missing authentication-related headers
- Generate:
  - Risk score (0–100)
  - Risk level (LOW / MEDIUM / HIGH)
  - Structured JSON output
  - Clean console output

---

##  Project Structure
- sec-phishing-emails-sim/
- │
- ├── pyproject.toml
- ├── README.md
- ├── src/
- │ └── phishing_sim/
- │ ├── cli.py
- │ └── analyzer/
- │ ├── parse_eml.py
- │ ├── url_features.py
- │ ├── header_features.py
- │ ├── scoring.py
- │ └── report.py
- └── tests/

---

##  Installation

Clone repository:

git clone https://github.com/YOUR_USERNAME/sec-phishing-emails-sim.git

cd sec-phishing-emails-sim


Create virtual environment:

python -m venv .venv
source .venv/Scripts/activate # Windows Git Bash
or

.venv\Scripts\activate # Windows CMD


Install project:

python -m pip install --upgrade pip
python -m pip install -e .


---

##  Usage

Analyze an email:

phishsim analyze samples/test.eml --pretty


Output example:

Risk score: 65/100 | Level: MEDIUM

Top reasons:

    URL shortener used

    Reply-To domain differs from From domain

    Urgency language in subject

URLs found:

    http://bit.ly/example


Generate JSON report:

phishsim analyze samples/test.eml --json report.json


---

##  Scoring Model

The risk score is based on weighted heuristics:

| Signal | Points |
|--------|--------|
| URL shortener | +20 |
| IP-based URL | +25 |
| Many links | +10 |
| Reply-To mismatch | +15 |
| Urgency subject | +10 |
| Missing auth headers | +10 |

Score is capped between 0–100.

---

##  Purpose

This project is designed for:

- Security training
- SOC skill development
- Email forensic practice
- Defensive security research

It does not send emails and does not simulate real-world phishing attacks.

---

##  Security Note

This tool performs offline analysis only.
It does not contact external services.

---

##  License

MIT License
