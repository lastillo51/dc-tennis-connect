"""JSON API compatibility tests for DC Tennis Connect."""

import os
from urllib.parse import parse_qs, urlparse

import pytest
from fastapi.testclient import TestClient

from app.main import app

from unittest.mock import patch

from app.api.schemas.court import Court, CourtLocation


db_required = pytest.mark.skipif(
    os.getenv("RUN_DB_TESTS") != "1",
    reason="Set RUN_DB_TESTS=1 for PostgreSQL-backed tests",
)


def test_root_endpoint():
    with TestClient(app) as client:
        response = client.get("/")

    assert response.status_code == 200
    assert response.json()["application"] == "DC Tennis Connect"


def test_health_endpoint():
    with TestClient(app) as client:
        response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


@db_required
def test_list_all_courts(court_test_data):
    with TestClient(app) as client:
        response = client.get("/courts/")

    assert response.status_code == 200
    courts = response.json()
    assert len(courts) == 3
    assert courts[0]["name"] == "Sample Court A"
    assert all("location" in court for court in courts)


@db_required
def test_filter_public_courts(court_test_data):
    with TestClient(app) as client:
        response = client.get("/courts/", params={"public_only": "true"})

    assert response.status_code == 200
    courts = response.json()
    assert len(courts) == 2
    assert all(court["public_access"] for court in courts)


@db_required
def test_get_court_by_id(court_test_data):
    with TestClient(app) as client:
        response = client.get("/courts/1")

    assert response.status_code == 200
    court = response.json()
    assert court["id"] == 1
    assert court["name"] == "Sample Court A"
    assert court["location"]["address"] == "Example Address A, Washington, DC"

    parsed = urlparse(court["google_maps_url"])
    parameters = parse_qs(parsed.query)
    assert parsed.scheme == "https"
    assert parsed.netloc == "www.google.com"
    assert parsed.path == "/maps/dir/"
    assert parameters["api"] == ["1"]
    assert parameters["destination"][0]


@db_required
def test_nonexistent_court(court_test_data):
    with TestClient(app) as client:
        response = client.get("/courts/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Court not found"


@db_required
def test_invalid_court_id(court_test_data):
    with TestClient(app) as client:
        response = client.get("/courts/abc")

    assert response.status_code == 422


@db_required
def test_invalid_public_only_parameter(court_test_data):
    with TestClient(app) as client:
        response = client.get("/courts/", params={"public_only": "invalid"})

    assert response.status_code == 422


def test_court_api_supports_unknown_reservation_policy():
    """API responses preserve null for unknown official policy."""

    fictional_court = Court(
        id=98765,
        name="Fictional API Test Court",
        location=CourtLocation(
            address="Example Address, Washington, DC",
            latitude=38.9,
            longitude=-77.0,
        ),
        number_of_courts=1,
        public_access=True,
        reservation_required=None,
    )

    with patch(
        "app.api.routes.courts.get_court_by_id",
        return_value=fictional_court,
    ):
        with TestClient(app) as client:
            response = client.get("/courts/98765")

    assert response.status_code == 200

    data = response.json()

    assert "reservation_required" in data
    assert data["reservation_required"] is None