"""Validate reviewed DPR facility import approvals."""

import json
from datetime import datetime
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, HttpUrl


class FacilityApproval(BaseModel):
    model_config = ConfigDict(extra="forbid")

    source_identifier: str = Field(
        pattern=r"^DPR_[0-9]+$",
        max_length=200,
    )
    public_access: Literal[True]
    evidence_url: HttpUrl
    verified_at: datetime

    @property
    def verified(self) -> bool:
        return (
            self.verified_at.tzinfo is not None
            and self.verified_at.utcoffset() is not None
        )


class ApprovalManifest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    schema_version: Literal[1]
    source_name: Literal["dcgis-dpr-parks"]
    approved_facilities: list[FacilityApproval]


def load_approvals(path: Path) -> ApprovalManifest:
    """Load approvals; reject duplicate IDs and invalid evidence."""

    data = json.loads(path.read_text(encoding="utf-8"))
    manifest = ApprovalManifest.model_validate(data)

    identifiers = [
        item.source_identifier
        for item in manifest.approved_facilities
    ]

    if len(identifiers) != len(set(identifiers)):
        raise ValueError("Duplicate approval identifiers")

    for item in manifest.approved_facilities:
        if not item.verified:
            raise ValueError("Approval timestamp must be timezone-aware")

        if item.evidence_url.scheme != "https":
            raise ValueError("Approval evidence must use HTTPS")

    return manifest