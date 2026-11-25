"""Convert persistent court records to public API schemas."""

from app.api.schemas.court import (
    AvailabilityStatus,
    Court,
    CourtLocation,
)
from app.db.models import Court as CourtModel


def court_to_schema(court: CourtModel) -> Court:
    """Map a database court into the existing Pydantic contract."""

    sources = sorted(
        court.sources,
        key=lambda source: source.id,
    )

    source_url = (
        sources[0].source_url
        if sources
        else None
    )

    return Court(
        id=court.id,
        name=court.name,
        location=CourtLocation(
            address=court.address,
            latitude=court.latitude,
            longitude=court.longitude,
        ),
        number_of_courts=court.number_of_courts,
        public_access=court.public_access,
        availability_status=AvailabilityStatus(
            court.availability_status
        ),
        operating_hours=None,
        reservation_required=court.reservation_required,
        source_url=source_url,
        google_maps_url=None,
    )