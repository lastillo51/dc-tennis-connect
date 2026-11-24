"""Validated DC GIS source records for court imports."""

from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    field_validator,
    model_validator,
)


class DPRCourtCandidate(BaseModel):
    """Normalized DPR facility awaiting import approval."""

    model_config = ConfigDict(extra="forbid")

    source_name: Literal["dcgis-dpr-parks"] = "dcgis-dpr-parks"

    source_identifier: str = Field(
        min_length=1,
        max_length=200,
    )

    global_id: UUID
    object_id: int = Field(gt=0)

    name: str = Field(min_length=1, max_length=100)
    address: str = Field(min_length=1, max_length=200)

    number_of_courts: int = Field(ge=1)

    active: bool | None = None
    use_type: str | None = Field(default=None, max_length=100)
    source_edited_at: datetime | None = None

    # Unknown information remains unknown.
    public_access: bool | None = None

    # Community scheduling does not depend on this policy.
    reservation_required: bool | None = None

    # Source validation is not operating-hours verification.
    availability_status: Literal["unknown"] = "unknown"

    @field_validator("source_identifier", "name", "address")
    @classmethod
    def strip_required_text(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Value cannot be blank")
        return value

    @model_validator(mode="after")
    def validate_review_state(self):
        # These fields must not be inferred from ACTIVE.
        return self

    @property
    def requires_review(self) -> bool:
        return (
            self.active is not True
            or self.public_access is None
        )