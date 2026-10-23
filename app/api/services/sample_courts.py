from datetime import time

from app.api.schemas.court import (
    AvailabilityStatus,
    Court,
    CourtHours,
    CourtLocation,
)


sample_courts = [
    Court(
        id=1,
        name="Sample Court A",
        location=CourtLocation(
            address="Example Address A, Washington, DC",
        ),
        number_of_courts=2,
        public_access=True,
        availability_status=AvailabilityStatus.FIRST_COME_FIRST_SERVED,
        operating_hours=CourtHours(
            opening_time=time(8, 0),
            closing_time=time(20, 0),
        ),
        reservation_required=False,
    ),
    Court(
        id=2,
        name="Sample Court B",
        location=CourtLocation(
            address="Example Address B, Washington, DC",
        ),
        number_of_courts=4,
        public_access=True,
        availability_status=AvailabilityStatus.PUBLISHED_HOURS,
        operating_hours=CourtHours(
            opening_time=time(7, 0),
            closing_time=time(21, 0),
        ),
        reservation_required=False,
    ),
    Court(
        id=3,
        name="Sample Court C",
        location=CourtLocation(
            address="Example Address C, Washington, DC",
        ),
        number_of_courts=1,
        public_access=False,
        availability_status=AvailabilityStatus.UNKNOWN,
        operating_hours=None,
        reservation_required=True,
    ),
]