from urllib.parse import parse_qs, urlparse

from app.api.schemas.court import CourtLocation
from app.api.services.maps_service import build_google_maps_url


def test_maps_url_uses_address():
    location = CourtLocation(
        address="Washington, DC",
    )

    url = build_google_maps_url(location)

    parsed = urlparse(url)
    query = parse_qs(parsed.query)

    assert parsed.scheme == "https"
    assert parsed.netloc == "www.google.com"
    assert parsed.path == "/maps/dir/"
    assert query["api"] == ["1"]
    assert query["destination"] == ["Washington, DC"]


def test_maps_url_uses_coordinates():
    location = CourtLocation(
        address="Example Address",
        latitude=38.8895,
        longitude=-77.0353,
    )

    url = build_google_maps_url(location)

    parsed = urlparse(url)
    query = parse_qs(parsed.query)

    assert query["destination"] == ["38.8895,-77.0353"]


def test_maps_url_falls_back_to_address():
    location = CourtLocation(
        address="Example Court, Washington, DC",
        latitude=38.8895,
        longitude=None,
    )

    url = build_google_maps_url(location)

    parsed = urlparse(url)
    query = parse_qs(parsed.query)

    assert query["destination"] == [
        "Example Court, Washington, DC"
    ]