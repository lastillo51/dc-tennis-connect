"""Read-only database lookups for DPR court imports."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models.court import Court, CourtSource
from app.importers.planner import ExistingCourt


SOURCE_NAME = "dcgis-dpr-parks"


def load_existing_courts(
    db: Session,
) -> dict[str, ExistingCourt]:
    """Load existing DPR source identities without modifying data."""

    statement = (
        select(CourtSource, Court)
        .join(Court, Court.id == CourtSource.court_id)
        .where(CourtSource.source_name == SOURCE_NAME)
        .where(CourtSource.source_identifier.is_not(None))
    )

    existing = {}

    for source, court in db.execute(statement).all():
        identifier = source.source_identifier

        if identifier in existing:
            raise ValueError(
                "Duplicate source identity in database"
            )

        existing[identifier] = ExistingCourt(
            source_identifier=identifier,
            name=court.name,
            address=court.address,
            number_of_courts=court.number_of_courts,
        )

    return existing