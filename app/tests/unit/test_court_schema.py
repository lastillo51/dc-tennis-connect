import pytest
from pydantic import ValidationError

from app.api.schemas.court import (
    AvailabilityStatus,
    Court,
    CourtLocation,
)


def test_valid_court():
    court = Court(
        id=1,
        name="Sample Court",
        location=CourtLocation(
            address="Example Address, Washington, DC",
        ),
        number_of_courts=2,
        public_access=True,
    )

    assert court.id == 1
    assert court.name == "Sample Court"
    assert court.availability_status == AvailabilityStatus.UNKNOWN


def test_invalid_court_id():
    with pytest.raises(ValidationError):
        Court(
            id=0,
            name="Sample Court",
            location=CourtLocation(
                address="Example Address, Washington, DC",
            ),
            number_of_courts=2,
            public_access=True,
        )


def test_invalid_number_of_courts():
    with pytest.raises(ValidationError):
        Court(
            id=1,
            name="Sample Court",
            location=CourtLocation(
                address="Example Address, Washington, DC",
            ),
            number_of_courts=0,
            public_access=True,
        )


def test_invalid_latitude():
    with pytest.raises(ValidationError):
        CourtLocation(
            address="Example Address, Washington, DC",
            latitude=100.0,
        )


def test_invalid_longitude():
    with pytest.raises(ValidationError):
        CourtLocation(
            address="Example Address, Washington, DC",
            longitude=-200.0,
        )