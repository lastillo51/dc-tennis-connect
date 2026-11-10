from html import unescape
from urllib.parse import parse_qs, urlparse

from fastapi.testclient import TestClient

from app.main import app
from app.api.services.court_service import get_all_courts
from app.api.services.maps_service import build_google_maps_url

import pytest

from unittest.mock import patch


client = TestClient(app)


def test_court_detail_returns_html():
    court = get_all_courts()[0]

    response = client.get(f"/web/courts/{court.id}")

    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]


def test_court_detail_displays_name_and_address():
    court = get_all_courts()[0]

    response = client.get(f"/web/courts/{court.id}")

    assert response.status_code == 200
    assert court.name in response.text
    assert court.location.address in response.text


def test_court_detail_displays_availability_disclaimer():
    court = get_all_courts()[0]

    response = client.get(f"/web/courts/{court.id}")

    assert response.status_code == 200

    normalized_html = " ".join(response.text.split())

    assert (
        "do not guarantee physical court availability"
        in normalized_html
    )


def test_unknown_court_returns_404():
    response = client.get("/web/courts/99999")

    assert response.status_code == 404


def test_invalid_court_id_returns_422():
    response = client.get("/web/courts/not-a-number")

    assert response.status_code == 422


def test_directory_links_to_court_detail():
    court = get_all_courts()[0]

    response = client.get("/web/courts")

    assert response.status_code == 200
    assert f'href="/web/courts/{court.id}"' in response.text


def test_court_detail_displays_google_maps_link():
    court = get_all_courts()[0]

    response = client.get(f"/web/courts/{court.id}")

    assert response.status_code == 200
    assert "Get Google Maps Directions" in response.text

    expected_url = build_google_maps_url(court.location)

    assert expected_url in unescape(response.text)


def test_google_maps_url_uses_expected_destination():
    court = get_all_courts()[0]

    url = build_google_maps_url(court.location)

    parsed = urlparse(url)
    parameters = parse_qs(parsed.query)

    assert parsed.scheme == "https"
    assert parsed.netloc == "www.google.com"
    assert parsed.path == "/maps/dir/"
    assert parameters["api"] == ["1"]


    if (
        court.location.latitude is not None
        and court.location.longitude is not None
    ):
        expected_destination = (
            f"{court.location.latitude},"
            f"{court.location.longitude}"
        )
    else:
        expected_destination = court.location.address

    assert parameters["destination"] == [expected_destination]


def test_court_detail_displays_court_information():
    court = get_all_courts()[0]

    response = client.get(f"/web/courts/{court.id}")

    assert response.status_code == 200

    html = " ".join(response.text.split())

    assert "Number of courts" in html
    assert str(court.number_of_courts) in html
    assert "Public access" in html
    assert "Availability classification" in html
    assert "Reservation required" in html

def test_court_detail_handles_operating_hours():
    court = get_all_courts()[0]

    response = client.get(f"/web/courts/{court.id}")

    assert response.status_code == 200

    normalized_html = " ".join(response.text.split())

    if court.operating_hours is None:
        assert (
            "Operating hours are not currently available."
            in normalized_html
        )
    else:
        opening_time = (
            court.operating_hours.opening_time.strftime("%I:%M %p")
        )

        closing_time = (
            court.operating_hours.closing_time.strftime("%I:%M %p")
        )

        assert opening_time in normalized_html
        assert closing_time in normalized_html

@pytest.mark.parametrize(
    "court",
    get_all_courts(),
    ids=lambda court: f"court-{court.id}",
)
def test_all_sample_courts_have_detail_pages(court):
    response = client.get(f"/web/courts/{court.id}")

    assert response.status_code == 200
    assert court.name in response.text
    assert court.location.address in response.text


from unittest.mock import patch


def test_court_detail_template_escapes_court_name():
    original_court = get_all_courts()[0]

    unsafe_name = "<script>alert('test')</script>"

    test_court = original_court.model_copy(
        update={"name": unsafe_name}
    )

    with patch(
        "app.web.routes.get_court_by_id",
        return_value=test_court,
    ):
        response = client.get(
            f"/web/courts/{original_court.id}"
        )

    assert response.status_code == 200

    # The raw script must not appear in rendered HTML.
    assert unsafe_name not in response.text

    # Jinja2 should escape the HTML markup.
    assert "&lt;script&gt;" in response.text
    assert "&lt;/script&gt;" in response.text

def test_court_detail_escapes_address():
    original_court = get_all_courts()[0]

    unsafe_address = "<script>alert('address')</script>"

    test_location = original_court.location.model_copy(
        update={"address": unsafe_address}
    )

    test_court = original_court.model_copy(
        update={"location": test_location}
    )

    with patch(
        "app.web.routes.get_court_by_id",
        return_value=test_court,
    ):
        response = client.get(
            f"/web/courts/{original_court.id}"
        )

    assert response.status_code == 200
    assert unsafe_address not in response.text
    assert "&lt;script&gt;" in response.text
    assert "&lt;/script&gt;" in response.text

def test_google_maps_url_cannot_use_javascript_scheme():
    court = get_all_courts()[0]

    malicious_location = court.location.model_copy(
        update={
            "address": "javascript:alert('xss')",
            "latitude": None,
            "longitude": None,
        }
    )

    url = build_google_maps_url(malicious_location)
    parsed = urlparse(url)

    assert parsed.scheme == "https"
    assert parsed.netloc == "www.google.com"
    assert parsed.path == "/maps/dir/"
    assert "javascript:" not in url.split("?")[0]