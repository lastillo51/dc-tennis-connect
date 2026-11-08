from pathlib import Path

from fastapi import APIRouter, Request, Query
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.api.services.court_service import search_courts

from fastapi import HTTPException

from app.api.services.court_service import get_court_by_id

from app.api.services.maps_service import build_google_maps_url

BASE_DIR = Path(__file__).resolve().parents[1]

templates = Jinja2Templates(
    directory=str(BASE_DIR / "templates")
)

router = APIRouter(
    prefix="/web",
    tags=["web"],
)


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
    q: str = Query(default="", max_length=100),
    public_only: bool = False,
):
    courts = search_courts(
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

@router.get("/courts/{court_id}", response_class=HTMLResponse)
def court_detail(request: Request, court_id: int):
    court = get_court_by_id(court_id)

    if court is None:
        raise HTTPException(
            status_code=404,
            detail="Court not found",
        )

    google_maps_url = build_google_maps_url(court.location)

    return templates.TemplateResponse(
        request=request,
        name="courts/detail.html",
        context={
            "page_title": court.name,
            "court": court,
            "google_maps_url": google_maps_url,
        },
    )