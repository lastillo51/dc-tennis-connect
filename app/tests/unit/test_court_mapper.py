
"""Unit tests for ORM-to-Pydantic court mapping."""

from app.api.mappers.court_mapper import court_to_schema
from app.api.schemas.court import AvailabilityStatus
from app.db.models import Court as CourtModel


def test_mapper_preserves_court_fields():
    record = CourtModel(
        id=1,
        name="Test Court",
        address="Test Address, Washington, DC",
        latitude=38.9,
        longitude=-77.0,
        number_of_courts=2,
        public_access=True,
        availability_status="unknown",
        reservation_required=False,
        sources=[],
    )

    court = court_to_schema(record)

    assert court.id == 1
    assert court.name == "Test Court"
    assert court.location.address == record.address
    assert court.location.latitude == 38.9
    assert court.location.longitude == -77.0
    assert court.number_of_courts == 2
    assert court.availability_status == AvailabilityStatus.UNKNOWN
    assert court.operating_hours is None
    assert court.google_maps_url is None


def test_mapper_preserves_unknown_reservation_policy():
    """Unknown official reservation policies remain None."""

    record = CourtModel(
        id=2,
        name="Fictional Test Court",
        address="Example Address, Washington, DC",
        latitude=38.9,
        longitude=-77.0,
        number_of_courts=2,
        public_access=True,
        availability_status="unknown",
        reservation_required=None,
        sources=[],
    )

    court = court_to_schema(record)

    assert court.reservation_required is None
    assert court.model_dump(mode="json")["reservation_required"] is None