from fastapi.testclient import TestClient

from app.main import app
from app.api.services.court_service import get_all_courts


client = TestClient(app)


def test_homepage_contains_main_landmark():
    response = client.get("/web")

    assert response.status_code == 200
    assert '<main id="main-content">' in response.text


def test_homepage_contains_skip_link():
    response = client.get("/web")

    assert response.status_code == 200
    assert 'href="#main-content"' in response.text
    assert "Skip to main content" in response.text


def test_directory_search_has_label():
    response = client.get("/web/courts")

    assert response.status_code == 200
    assert 'for="court-search"' in response.text
    assert 'id="court-search"' in response.text


def test_court_detail_has_primary_heading():
    court = get_all_courts()[0]

    response = client.get(f"/web/courts/{court.id}")

    assert response.status_code == 200
    assert "<h1>" in response.text
    assert court.name in response.text


def test_external_maps_link_has_security_attributes():
    court = get_all_courts()[0]

    response = client.get(f"/web/courts/{court.id}")

    assert response.status_code == 200
    assert 'target="_blank"' in response.text
    assert 'rel="noopener noreferrer"' in response.text