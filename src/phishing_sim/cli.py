from __future__ import annotations

import argparse
from pathlib import Path
import json
import sys

from phishing_sim.analyzer.report import analyze_eml_to_report


def main() -> None:
    p = argparse.ArgumentParser(prog="phishsim", description="Defensive phishing email analyzer")
    sub = p.add_subparsers(dest="cmd", required=True)

    a = sub.add_parser("analyze", help="Analyze a .eml file and output a risk report")
    a.add_argument("eml", type=Path, help="Path to .eml file")
    a.add_argument("--json", dest="json_out", type=Path, help="Write JSON report to file")
    a.add_argument("--pretty", action="store_true", help="Pretty-print to console")

    args = p.parse_args()

    # Partial implementation f
    if not args.eml.exists():
        print(f"Error: file not found: {args.eml}")
        sys.exit(2)
    if args.eml.suffix.lower() != ".eml":
        print("Error: please provide a .eml file")
        sys.exit(2)

    if args.cmd == "analyze":
        report = analyze_eml_to_report(args.eml)

        if args.json_out:
            args.json_out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

        if args.pretty or not args.json_out:
            # nice console output
            print(f"Risk score: {report['score']}/100  |  Level: {report['level']}")
            print("Top reasons:")
            for r in report["top_reasons"]:
                print(f" - {r}")
            if report["urls"]:
                print("\nURLs found:")
                for u in report["urls"]:
                    print(f" - {u}")

if __name__ == "__main__":
    main()
