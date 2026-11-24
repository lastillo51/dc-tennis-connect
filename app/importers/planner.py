"""Read-only import planning for validated DPR court candidates."""

from dataclasses import dataclass
from enum import Enum
from typing import Iterable

from app.importers.schemas import DPRCourtCandidate


class ImportAction(str, Enum):
    INSERT = "insert"
    UPDATE = "update"
    UNCHANGED = "unchanged"
    REVIEW = "review"


@dataclass(frozen=True)
class ExistingCourt:
    source_identifier: str
    name: str
    address: str
    number_of_courts: int


@dataclass(frozen=True)
class PlannedImport:
    source_identifier: str
    action: ImportAction
    reason: str


def plan_import(
    candidates: Iterable[DPRCourtCandidate],
    existing: dict[str, ExistingCourt],
) -> list[PlannedImport]:
    """Plan changes without accessing or modifying PostgreSQL."""

    plans = []
    seen = set()

    for candidate in candidates:
        identifier = candidate.source_identifier

        if identifier in seen:
            plans.append(
                PlannedImport(
                    identifier,
                    ImportAction.REVIEW,
                    "Duplicate source identity in input batch",
                )
            )
            continue

        seen.add(identifier)

        if candidate.requires_review:
            plans.append(
                PlannedImport(
                    identifier,
                    ImportAction.REVIEW,
                    "Public access or operational status unverified",
                )
            )
            continue

        previous = existing.get(identifier)

        if previous is None:
            action = ImportAction.INSERT
            reason = "New approved source identity"

        elif (
            previous.name == candidate.name
            and previous.address == candidate.address
            and previous.number_of_courts
            == candidate.number_of_courts
        ):
            action = ImportAction.UNCHANGED
            reason = "No relevant changes detected"

        else:
            action = ImportAction.REVIEW
            reason = (
                "Existing court attributes changed; "
                "manual approval required before update"
            )

        plans.append(
            PlannedImport(identifier, action, reason)
        )

    return plans