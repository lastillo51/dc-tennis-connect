"""Court detail frontend compatibility and security tests."""

import os
from html import unescape
from unittest.mock import patch
from urllib.parse import parse_qs, urlparse

import pytest
from fastapi.testclient import TestClient

from app.api.services.court_service import get_all_courts
from app.api.services.maps_service import build_google_maps_url
from app.main import app

pytestmark = pytest.mark.skipif(
    os.getenv("RUN_DB_TESTS") != "1",
    reason="Set RUN_DB_TESTS=1 for PostgreSQL-backed tests",
)


def first_court(court_test_data):
    return get_all_courts(court_test_data)[0]


def test_court_detail_returns_html(court_test_data):
    court = first_court(court_test_data)
    with TestClient(app) as client:
        response = client.get(f"/web/courts/{court.id}")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]


def test_court_detail_displays_name_and_address(court_test_data):
    court = first_court(court_test_data)
    with TestClient(app) as client:
        response = client.get(f"/web/courts/{court.id}")
    assert response.status_code == 200
    assert court.name in response.text
    assert court.location.address in response.text


def test_court_detail_displays_availability_disclaimer(court_test_data):
    court = first_court(court_test_data)
    with TestClient(app) as client:
        response = client.get(f"/web/courts/{court.id}")
    assert response.status_code == 200
    assert "do not guarantee physical court availability" in " ".join(response.text.split())


def test_unknown_court_returns_404(court_test_data):
    with TestClient(app) as client:
        response = client.get("/web/courts/99999")
    assert response.status_code == 404


def test_invalid_court_id_returns_422(court_test_data):
    with TestClient(app) as client:
        response = client.get("/web/courts/not-a-number")
    assert response.status_code == 422


def test_directory_links_to_court_detail(court_test_data):
    court = first_court(court_test_data)
    with TestClient(app) as client:
        response = client.get("/web/courts")
    assert response.status_code == 200
    assert f'href="/web/courts/{court.id}"' in response.text


def test_court_detail_displays_google_maps_link(court_test_data):
    court = first_court(court_test_data)
    with TestClient(app) as client:
        response = client.get(f"/web/courts/{court.id}")
    assert response.status_code == 200
    assert "Get Google Maps Directions" in response.text
    assert build_google_maps_url(court.location) in unescape(response.text)


def test_google_maps_url_uses_expected_destination(court_test_data):
    court = first_court(court_test_data)
    parsed = urlparse(build_google_maps_url(court.location))
    parameters = parse_qs(parsed.query)
    assert parsed.scheme == "https"
    assert parsed.netloc == "www.google.com"
    assert parsed.path == "/maps/dir/"
    assert parameters["api"] == ["1"]
    if court.location.latitude is not None and court.location.longitude is not None:
        expected = f"{court.location.latitude},{court.location.longitude}"
    else:
        expected = court.location.address
    assert parameters["destination"] == [expected]


def test_court_detail_displays_court_information(court_test_data):
    court = first_court(court_test_data)
    with TestClient(app) as client:
        response = client.get(f"/web/courts/{court.id}")
    assert response.status_code == 200
    html = " ".join(response.text.split())
    for label in ("Number of courts", "Public access", "Availability classification", "Reservation required"):
        assert label in html
    assert str(court.number_of_courts) in html


def test_court_detail_handles_operating_hours(court_test_data):
    court = first_court(court_test_data)
    with TestClient(app) as client:
        response = client.get(f"/web/courts/{court.id}")
    assert response.status_code == 200
    html = " ".join(response.text.split())
    if court.operating_hours is None:
        assert "Operating hours are not currently available." in html
    else:
        assert court.operating_hours.opening_time.strftime("%I:%M %p") in html
        assert court.operating_hours.closing_time.strftime("%I:%M %p") in html


@pytest.mark.parametrize("court_index", [0, 1, 2])
def test_all_sample_courts_have_detail_pages(court_test_data, court_index):
    courts = get_all_courts(court_test_data)
    assert len(courts) == 3
    court = courts[court_index]
    with TestClient(app) as client:
        response = client.get(f"/web/courts/{court.id}")
    assert response.status_code == 200
    assert court.name in response.text
    assert court.location.address in response.text


def test_court_detail_template_escapes_court_name(court_test_data):
    original = first_court(court_test_data)
    unsafe_name = "<script>alert('test')</script>"
    modified = original.model_copy(update={"name": unsafe_name})
    with patch("app.web.routes.get_court_by_id", return_value=modified):
        with TestClient(app) as client:
            response = client.get(f"/web/courts/{original.id}")
    assert response.status_code == 200
    assert unsafe_name not in response.text
    assert "&lt;script&gt;" in response.text
    assert "&lt;/script&gt;" in response.text


def test_court_detail_escapes_address(court_test_data):
    original = first_court(court_test_data)
    unsafe_address = "<script>alert('address')</script>"
    location = original.location.model_copy(update={"address": unsafe_address})
    modified = original.model_copy(update={"location": location})
    with patch("app.web.routes.get_court_by_id", return_value=modified):
        with TestClient(app) as client:
            response = client.get(f"/web/courts/{original.id}")
    assert response.status_code == 200
    assert unsafe_address not in response.text
    assert "&lt;script&gt;" in response.text
    assert "&lt;/script&gt;" in response.text


def test_google_maps_url_cannot_use_javascript_scheme(court_test_data):
    court = first_court(court_test_data)
    location = court.location.model_copy(update={
        "address": "javascript:alert('xss')", "latitude": None, "longitude": None,
    })
    url = build_google_maps_url(location)
    parsed = urlparse(url)
    assert parsed.scheme == "https"
    assert parsed.netloc == "www.google.com"
    assert parsed.path == "/maps/dir/"
    assert "javascript:" not in url.split("?")[0]