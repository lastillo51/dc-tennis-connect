"""Server-rendered frontend routes."""

from pathlib import Path
from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query,
    Request,
)
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.api.services.court_service import (
    get_court_by_id,
    search_courts,
)
from app.api.services.maps_service import build_google_maps_url
from app.db.session import get_db


BASE_DIR = Path(__file__).resolve().parents[1]

templates = Jinja2Templates(
    directory=str(BASE_DIR / "templates")
)

router = APIRouter(
    prefix="/web",
    tags=["web"],
)

DbSession = Annotated[Session, Depends(get_db)]


@router.get("", response_class=HTMLResponse)
def homepage(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="home.html",
        context={
            "page_title": "DC Tennis Connect",
        },
    )


@router.get("/courts", response_class=HTMLResponse)
def court_directory(
    request: Request,
    db: DbSession,
    q: str = Query(default="", max_length=100),
    public_only: bool = False,
):
    courts = search_courts(
        db,
        query=q,
        public_only=public_only,
    )

    return templates.TemplateResponse(
        request=request,
        name="courts/index.html",
        context={
            "page_title": "Explore Courts",
            "courts": courts,
            "search_query": q,
            "public_only": public_only,
            "result_count": len(courts),
        },
    )


@router.get(
    "/courts/{court_id}",
    response_class=HTMLResponse,
)
def court_detail(
    request: Request,
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

    google_maps_url = build_google_maps_url(
        court.location
    )

    return templates.TemplateResponse(
        request=request,
        name="courts/detail.html",
        context={
            "page_title": court.name,
            "court": court,
            "google_maps_url": google_maps_url,
        },
    )