"""Court directory frontend compatibility tests."""

import os

import pytest
from fastapi.testclient import TestClient

from app.main import app

pytestmark = pytest.mark.skipif(
    os.getenv("RUN_DB_TESTS") != "1",
    reason="Set RUN_DB_TESTS=1 for PostgreSQL-backed tests",
)


def test_directory_returns_html(court_test_data):
    with TestClient(app) as client:
        response = client.get("/web/courts")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]


def test_directory_displays_sample_courts(court_test_data):
    with TestClient(app) as client:
        response = client.get("/web/courts")
    assert response.status_code == 200
    assert "3 courts found" in response.text


def test_public_only_filter(court_test_data):
    with TestClient(app) as client:
        response = client.get("/web/courts", params={"public_only": "true"})
    assert response.status_code == 200
    assert "2 courts found" in response.text


def test_search_returns_empty_state(court_test_data):
    with TestClient(app) as client:
        response = client.get("/web/courts", params={"q": "unlikely-name-12345"})
    assert response.status_code == 200
    assert "No courts found" in response.text


def test_invalid_boolean_is_rejected(court_test_data):
    with TestClient(app) as client:
        response = client.get("/web/courts", params={"public_only": "invalid"})
    assert response.status_code == 422


def test_excessively_long_query_is_rejected(court_test_data):
    with TestClient(app) as client:
        response = client.get("/web/courts", params={"q": "a" * 101})
    assert response.status_code == 422


def test_directory_has_search_form(court_test_data):
    with TestClient(app) as client:
        response = client.get("/web/courts")
    assert response.status_code == 200
    assert 'name="q"' in response.text
    assert 'name="public_only"' in response.text