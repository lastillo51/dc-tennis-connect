"""Database queries for persistent tennis court records."""

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.db.models import Court as CourtModel


def get_all_courts(
    db: Session,
    public_only: bool = False,
) -> list[CourtModel]:
    """Retrieve court records in a deterministic order."""

    statement = (
        select(CourtModel)
        .options(selectinload(CourtModel.sources))
        .order_by(CourtModel.id)
    )

    if public_only:
        statement = statement.where(
            CourtModel.public_access.is_(True)
        )

    return list(db.scalars(statement).all())


def get_court_by_id(
    db: Session,
    court_id: int,
) -> CourtModel | None:
    """Retrieve a single court by its identifier."""

    statement = (
        select(CourtModel)
        .options(selectinload(CourtModel.sources))
        .where(CourtModel.id == court_id)
    )

    return db.scalar(statement)


def search_courts(
    db: Session,
    query: str = "",
    public_only: bool = False,
) -> list[CourtModel]:
    """Search court names and addresses."""

    statement = (
        select(CourtModel)
        .options(selectinload(CourtModel.sources))
    )

    if public_only:
        statement = statement.where(
            CourtModel.public_access.is_(True)
        )

    search = query.strip()

    if search:
        pattern = (
            "%"
            + search.replace("\\", "\\\\")
                    .replace("%", "\\%")
                    .replace("_", "\\_")
            + "%"
        )

        statement = statement.where(
            CourtModel.name.ilike(
                pattern, escape="\\"
            )
            | CourtModel.address.ilike(
                pattern, escape="\\"
            )
        )

    statement = statement.order_by(CourtModel.id)

    return list(db.scalars(statement).all())