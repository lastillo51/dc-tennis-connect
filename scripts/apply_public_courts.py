"""Controlled import of explicitly approved DPR facilities."""

import argparse
from datetime import datetime, timezone
from pathlib import Path

from app.importers.approvals import load_approvals
from app.importers.dcgis_adapter import load_dpr_candidates
from app.importers.service import import_approved_courts


ROOT = Path(__file__).resolve().parents[1]

DEFAULT_SOURCE = (
    ROOT / "data/source-evaluation/dpr-tennis-candidates.json"
)
DEFAULT_APPROVALS = (
    ROOT / "data/import-approvals/dpr-approved-courts.json"
)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser()

    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    parser.add_argument(
        "--approvals", type=Path, default=DEFAULT_APPROVALS
    )
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--database", required=True)

    args = parser.parse_args(argv)

    if not args.apply:
        print("FAIL: Explicit --apply required")
        return 1

    # This first implementation is restricted to the test database.
    if args.database != "dc_tennis_test":
        print("FAIL: Only dc_tennis_test is permitted")
        return 1

    try:
        manifest = load_approvals(args.approvals)
        result = load_dpr_candidates(args.source)

        if result["rejected"]:
            raise ValueError("Source batch contains rejected records")

        candidates_by_id = {
            item.source_identifier: item
            for item in result["valid"]
        }

        if len(candidates_by_id) != len(result["valid"]):
            raise ValueError("Duplicate source identifiers")

        approved = []

        for approval in manifest.approved_facilities:
            candidate = candidates_by_id.get(
                approval.source_identifier
            )

            if candidate is None:
                raise ValueError("Approved ID missing from source")

            if candidate.active is not True:
                raise ValueError("Facility activity unverified")

            if approval.verified_at > datetime.now(timezone.utc):
                raise ValueError("Future approval timestamp")

            approved.append(
                candidate.model_copy(
                    update={"public_access": True}
                )
            )

        if not approved:
            print("No approved facilities; no database changes")
            return 0

        from app.db.session import (
            get_engine,
            get_session_factory,
        )

        engine = get_engine()

        try:
            if engine.url.database != args.database:
                raise ValueError("Database identity mismatch")

            SessionLocal = get_session_factory()

            with SessionLocal.begin() as db:
                counts = import_approved_courts(
                    db,
                    approved,
                    apply=True,
                )

            print("Inserted:", counts["inserted"])
            print("Unchanged:", counts["unchanged"])
            return 0

        finally:
            engine.dispose()

    except Exception as exc:
        # Avoid printing exception details or database credentials.
        print("FAIL: Import aborted")
        print("Error category:", type(exc).__name__)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())