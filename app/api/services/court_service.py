from app.api.schemas.court import Court
from app.api.services.sample_courts import sample_courts


def get_all_courts(public_only: bool = False) -> list[Court]:
    if public_only:
        return [
            court
            for court in sample_courts
            if court.public_access
        ]

    return sample_courts


def get_court_by_id(court_id: int) -> Court | None:
    for court in sample_courts:
        if court.id == court_id:
            return court

    return None
