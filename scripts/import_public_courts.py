"""Read-only CLI for evaluating DC GIS tennis court imports."""

import argparse
from collections import Counter
from pathlib import Path

from sqlalchemy.exc import SQLAlchemyError

from app.importers.dcgis_adapter import load_dpr_candidates
from app.importers.planner import plan_import
from app.importers.repository import load_existing_courts


PROJECT_ROOT = Path(__file__).resolve().parents[1]

DEFAULT_SOURCE = (
    PROJECT_ROOT
    / "data"
    / "source-evaluation"
    / "dpr-tennis-candidates.json"
)

ALLOWED_DATABASES = {
    "dc_tennis_test",
    "dc_tennis_migration_test",
}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Preview DPR court imports without database writes."
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Explicitly request read-only evaluation (default).",
    )

    parser.add_argument(
        "--source",
        type=Path,
        default=DEFAULT_SOURCE,
        help="Path to a saved DC GIS Layer 9 JSON response.",
    )

    return parser


def run_dry_run(source_path: Path) -> int:
    """Validate candidates and compare against PostgreSQL."""

    if not source_path.is_file():
        print("FAIL: Source JSON file not found")
        return 1

    try:
        result = load_dpr_candidates(source_path)
    except (OSError, ValueError, TypeError) as exc:
        print("FAIL: Source validation could not complete")
        print("Error category:", type(exc).__name__)
        return 1

    valid = result["valid"]
    rejected = result["rejected"]

    # Never interpret a partial source response as an approved batch.
    if not valid:
        print("FAIL: No valid source records")
        return 1

    # Import lazily so source-validation tests do not require
    # a configured or running PostgreSQL server.
    from app.db.session import get_engine, get_session_factory

    engine = None

    try:
        engine = get_engine()

        database_name = engine.url.database

        if database_name not in ALLOWED_DATABASES:
            print("FAIL: Database is not approved for this CLI")
            return 1

        # Explicit read-only transaction at PostgreSQL level.
        with engine.connect().execution_options(
            isolation_level="READ COMMITTED"
        ) as connection:
            connection.exec_driver_sql(
                "SET TRANSACTION READ ONLY"
            )

            from sqlalchemy.orm import Session

            with Session(
                bind=connection,
                autoflush=False,
            ) as db:
                existing = load_existing_courts(db)

            # Roll back the read-only transaction on exit.
            connection.rollback()

        plans = plan_import(valid, existing)

    except (SQLAlchemyError, RuntimeError, ValueError) as exc:
        print("FAIL: Database comparison could not complete")
        print("Error category:", type(exc).__name__)
        return 1

    finally:
        if engine is not None:
            engine.dispose()

    counts = Counter(plan.action.value for plan in plans)

    print("DC Tennis Connect — Import Dry Run")
    print("----------------------------------")
    print("Database:", database_name)
    print("Source records:", result["total"])
    print("Valid candidates:", len(valid))
    print("Rejected candidates:", len(rejected))
    print(
        "Reported courts:",
        sum(item.number_of_courts for item in valid),
    )
    print("Existing source identities:", len(existing))

    for action in ("insert", "update", "unchanged", "review"):
        print(f"{action}: {counts.get(action, 0)}")

    if rejected:
        print("Rejected source record indices:")
        for item in rejected:
            print(
                f"  {item['index']}: {item['reason']}"
            )

    print("PASS: Dry-run comparison completed")
    print("No database changes were applied.")

    # Nonzero status prevents accepting a partially invalid batch.
    return 2 if rejected else 0


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    return run_dry_run(args.source)


if __name__ == "__main__":
    raise SystemExit(main())