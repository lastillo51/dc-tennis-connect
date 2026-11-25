"""Fictional court fixtures for isolated database tests."""

from sqlalchemy.orm import Session

from app.api.services.sample_courts import sample_courts
from app.db.models import Court as CourtModel


def seed_sample_courts(db: Session) -> None:
    """Insert the existing fictional sample courts."""

    for court in sample_courts:
        db.add(
            CourtModel(
                id=court.id,
                name=court.name,
                address=court.location.address,
                latitude=court.location.latitude,
                longitude=court.location.longitude,
                number_of_courts=court.number_of_courts,
                public_access=court.public_access,
                availability_status=court.availability_status.value,
                reservation_required=court.reservation_required,
            )
        )

    db.flush()