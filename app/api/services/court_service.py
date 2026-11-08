from app.api.schemas.court import Court
from app.api.services.sample_courts import sample_courts


def get_all_courts(public_only: bool = False) -> list[Court]:
    """Return all courts, optionally filtering by public access."""
    if public_only:
        return [
            court
            for court in sample_courts
            if court.public_access
        ]

    return sample_courts


def get_court_by_id(court_id: int) -> Court | None:
    """Return a court by its ID, or None if it does not exist."""
    for court in sample_courts:
        if court.id == court_id:
            return court

    return None


def search_courts(
    query: str = "",
    public_only: bool = False,
) -> list[Court]:
    """Search court names and addresses with optional public filtering."""

    courts = get_all_courts(public_only=public_only)
    search = query.strip().casefold()

    if not search:
        return courts

    return [
        court
        for court in courts
        if search in (
            f"{court.name} {court.location.address}"
        ).casefold()
    ]