from fastapi import APIRouter, HTTPException, Query

from app.api.schemas.court import Court
from app.api.services.court_service import (
    get_all_courts,
    get_court_by_id,
)
from app.api.services.maps_service import build_google_maps_url


router = APIRouter(
    prefix="/courts",
    tags=["Courts"],
)


@router.get("/", response_model=list[Court])
def list_courts(
    public_only: bool = Query(default=False),
):
    courts = get_all_courts(public_only=public_only)

    return [
        court.model_copy(
            update={
                "google_maps_url": build_google_maps_url(court.location)
            }
        )
        for court in courts
    ]


@router.get("/{court_id}", response_model=Court)
def get_court(court_id: int):
    court = get_court_by_id(court_id)

    if court is None:
        raise HTTPException(
            status_code=404,
            detail="Court not found",
        )

    return court.model_copy(
        update={
            "google_maps_url": build_google_maps_url(court.location)
        }
    )