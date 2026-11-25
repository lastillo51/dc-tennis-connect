"""Transactional import service for approved DPR court records."""

from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models.court import Court, CourtSource
from app.importers.schemas import DPRCourtCandidate


SOURCE_NAME = "dcgis-dpr-parks"

SOURCE_URL = (
    "https://maps2.dcgis.dc.gov/dcgis/rest/services/"
    "DCGIS_DATA/Recreation_WebMercator/MapServer/9"
)


def import_approved_courts(
    db: Session,
    candidates: Sequence[DPRCourtCandidate],
    *,
    apply: bool = False,
) -> dict[str, int]:
    """Stage approved inserts without committing the transaction.

    The caller must provide an active transaction and is responsible
    for committing or rolling back. Existing source records are
    preserved and are not automatically updated.
    """

    if not apply:
        raise ValueError(
            "Explicit apply=True is required for database writes"
        )

    if not db.in_transaction():
        raise ValueError(
            "An active database transaction is required"
        )

    seen = set()

    # Validate the entire batch before performing writes.
    for candidate in candidates:
        identity = (
            candidate.source_name,
            candidate.source_identifier,
        )

        if identity in seen:
            raise ValueError("Duplicate identity in import batch")

        seen.add(identity)

        if candidate.source_name != SOURCE_NAME:
            raise ValueError("Unexpected source namespace")

        if candidate.active is not True:
            raise ValueError("Facility activity is not verified")

        if candidate.public_access is not True:
            raise ValueError("Public access is not approved")


    inserted = 0
    unchanged = 0

    for candidate in candidates:
        existing_source = db.scalar(
            select(CourtSource).where(
                CourtSource.source_name == SOURCE_NAME,
                CourtSource.source_identifier
                == candidate.source_identifier,
            )
        )

        if existing_source is not None:
            unchanged += 1
            continue

        court = Court(
            name=candidate.name,
            address=candidate.address,
            number_of_courts=candidate.number_of_courts,
            public_access=True,
            availability_status="unknown",
            reservation_required=candidate.reservation_required,
        )

        source = CourtSource(
            source_name=SOURCE_NAME,
            source_identifier=candidate.source_identifier,
            source_url=SOURCE_URL,
            source_type="open_data",
            last_verified_at=None,
        )

        # Use explicit foreign-key association after flush.
        db.add(court)
        db.flush()

        source.court_id = court.id
        db.add(source)

        inserted += 1

    db.flush()

    return {
        "inserted": inserted,
        "unchanged": unchanged,
    }