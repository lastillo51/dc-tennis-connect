from datetime import time
from enum import Enum

from pydantic import BaseModel, Field


class AvailabilityStatus(str, Enum):
    PUBLISHED_HOURS = "published_hours"
    RESERVABLE = "reservable"
    FIRST_COME_FIRST_SERVED = "first_come_first_served"
    CLOSED = "closed"
    UNKNOWN = "unknown"


class CourtLocation(BaseModel):
    address: str = Field(min_length=1, max_length=200)
    latitude: float | None = Field(default=None, ge=-90, le=90)
    longitude: float | None = Field(default=None, ge=-180, le=180)


class CourtHours(BaseModel):
    opening_time: time
    closing_time: time


class Court(BaseModel):
    id: int = Field(gt=0)
    name: str = Field(min_length=1, max_length=100)
    location: CourtLocation
    number_of_courts: int = Field(ge=1)
    public_access: bool
    availability_status: AvailabilityStatus = AvailabilityStatus.UNKNOWN
    operating_hours: CourtHours | None = None
    reservation_required: bool = False
    source_url: str | None = None
    google_maps_url: str | None = None