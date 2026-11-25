"""Frontend and API tests using isolated PostgreSQL fixtures."""

import pytest
from fastapi.testclient import TestClient

from app.main import app


pytestmark = pytest.mark.skipif(
    __import__("os").getenv("RUN_DB_TESTS") != "1",
    reason="Set RUN_DB_TESTS=1 for PostgreSQL tests",
)


def test_database_backed_court_directory(court_test_data):
    with TestClient(app) as client:
        response = client.get("/web/courts")

    assert response.status_code == 200
    assert "3 courts found" in response.text


def test_database_backed_public_filter(court_test_data):
    with TestClient(app) as client:
        response = client.get(
            "/web/courts",
            params={"public_only": "true"},
        )

    assert response.status_code == 200
    assert "2 courts found" in response.text


def test_database_backed_json_api(court_test_data):
    with TestClient(app) as client:
        response = client.get("/courts/")

    assert response.status_code == 200

    courts = response.json()

    assert len(courts) == 3
    assert all("location" in court for court in courts)


def test_database_backed_missing_court(court_test_data):
    with TestClient(app) as client:
        response = client.get("/web/courts/999999")

    assert response.status_code == 404