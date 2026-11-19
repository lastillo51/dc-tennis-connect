"""Court service backed by the PostgreSQL repository."""

from sqlalchemy.orm import Session

from app.api.mappers.court_mapper import court_to_schema
from app.api.schemas.court import Court
from app.db.repositories import court_repository


def get_all_courts(
    db: Session,
    public_only: bool = False,
) -> list[Court]:
    """Return all courts, optionally filtering by public access."""

    records = court_repository.get_all_courts(
        db,
        public_only=public_only,
    )

    return [
        court_to_schema(record)
        for record in records
    ]


def get_court_by_id(
    db: Session,
    court_id: int,
) -> Court | None:
    """Return a court by ID, or None if it does not exist."""

    record = court_repository.get_court_by_id(
        db,
        court_id,
    )

    if record is None:
        return None

    return court_to_schema(record)


def search_courts(
    db: Session,
    query: str = "",
    public_only: bool = False,
) -> list[Court]:
    """Search court names and addresses."""

    records = court_repository.search_courts(
        db,
        query=query,
        public_only=public_only,
    )

    return [
        court_to_schema(record)
        for record in records
    ]