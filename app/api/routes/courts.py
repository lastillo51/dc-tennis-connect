"""JSON API routes for tennis courts."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.api.schemas.court import Court
from app.api.services.court_service import (
    get_all_courts,
    get_court_by_id,
)
from app.api.services.maps_service import build_google_maps_url
from app.db.session import get_db


router = APIRouter(
    prefix="/courts",
    tags=["Courts"],
)

DbSession = Annotated[Session, Depends(get_db)]


@router.get("/", response_model=list[Court])
def list_courts(
    db: DbSession,
    public_only: bool = Query(default=False),
):
    courts = get_all_courts(
        db,
        public_only=public_only,
    )

    return [
        court.model_copy(
            update={
                "google_maps_url": build_google_maps_url(
                    court.location
                )
            }
        )
        for court in courts
    ]


@router.get("/{court_id}", response_model=Court)
def get_court(
    court_id: int,
    db: DbSession,
):
    court = get_court_by_id(
        db,
        court_id,
    )

    if court is None:
        raise HTTPException(
            status_code=404,
            detail="Court not found",
        )

    return court.model_copy(
        update={
            "google_maps_url": build_google_maps_url(
                court.location
            )
        }
    )