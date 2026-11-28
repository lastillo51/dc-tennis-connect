"""Read-only reconciliation of DPR public-access reviews."""

import csv
import json
from collections import Counter
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

from app.importers.dcgis_adapter import load_dpr_candidates


ROOT = Path(__file__).resolve().parents[1]

SOURCE = (
    ROOT / "data/source-evaluation/dpr-tennis-candidates.json"
)

REVIEW = (
    ROOT / "data/source-evaluation/reviews/"
    "dpr-public-access-review.csv"
)

OUTPUT = (
    ROOT / "data/source-evaluation/reviews/"
    "dpr-reconciliation-report.json"
)

ALLOWED_DECISIONS = {"approved", "review", "excluded"}


def main() -> int:
    result = load_dpr_candidates(SOURCE)

    if result["rejected"]:
        raise ValueError("Source contains rejected candidates")

    candidates = {
        item.source_identifier: item
        for item in result["valid"]
    }

    if len(candidates) != len(result["valid"]):
        raise ValueError("Duplicate source identifiers")

    with REVIEW.open(newline="", encoding="utf-8") as file:
        rows = list(csv.DictReader(file))

    if len(rows) != len(candidates):
        raise ValueError("Review count differs from source")

    seen = set()
    findings = []
    decisions = Counter()

    for row in rows:
        identifier = row["source_identifier"]
        decision = row["decision"].strip().lower()

        if identifier in seen:
            raise ValueError("Duplicate review identifier")

        seen.add(identifier)

        if identifier not in candidates:
            raise ValueError("Unknown source identifier")

        if decision not in ALLOWED_DECISIONS:
            raise ValueError("Invalid review decision")

        candidate = candidates[identifier]
        issues = []

        evidence_url = row["evidence_url"].strip()
        verified_at = row["verified_at"].strip()
        notes = row["review_notes"].strip()

        if row["name"] != candidate.name:
            issues.append("Name differs from validated source")

        if row["address"] != candidate.address:
            issues.append("Address differs from validated source")

        if int(row["number_of_courts"]) != candidate.number_of_courts:
            issues.append("Court count differs from validated source")

        if decision == "approved":
            if candidate.active is not True:
                issues.append("Activity status is not confirmed")

            parsed = urlparse(evidence_url)

            if parsed.scheme != "https" or not parsed.hostname:
                issues.append("Valid HTTPS evidence URL required")

            try:
                timestamp = datetime.fromisoformat(
                    verified_at.replace("Z", "+00:00")
                )

                if timestamp.tzinfo is None:
                    issues.append("Timestamp lacks timezone")
            except ValueError:
                issues.append("Invalid verification timestamp")

            if not notes:
                issues.append("Approval explanation required")

        decisions[decision] += 1

        findings.append({
            "source_identifier": identifier,
            "name": candidate.name,
            "decision": decision,
            "evidence_url": evidence_url,
            "verified_at": verified_at,
            "review_notes": notes,
            "issues": issues,
        })

    if seen != set(candidates):
        raise ValueError("Review is missing source identifiers")

    report = {
        "source_records": len(candidates),
        "decisions": dict(decisions),
        "findings": findings,
    }

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(
        json.dumps(report, indent=2),
        encoding="utf-8",
    )

    invalid = [
        item for item in findings
        if item["issues"]
    ]

    print("Source candidates:", len(candidates))
    print("Decisions:", dict(decisions))
    print("Records with consistency issues:", len(invalid))
    print("Report:", OUTPUT)

    return 1 if invalid else 0


if __name__ == "__main__":
    raise SystemExit(main())