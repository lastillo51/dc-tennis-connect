from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_directory_returns_html():
    response = client.get("/web/courts")

    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]


def test_directory_displays_sample_courts():
    response = client.get("/web/courts")

    assert response.status_code == 200
    assert "3 courts found" in response.text


def test_public_only_filter():
    response = client.get(
        "/web/courts",
        params={"public_only": "true"},
    )

    assert response.status_code == 200
    assert "2 courts found" in response.text


def test_search_returns_empty_state():
    response = client.get(
        "/web/courts",
        params={"q": "unlikely-name-12345"},
    )

    assert response.status_code == 200
    assert "No courts found" in response.text


def test_invalid_boolean_is_rejected():
    response = client.get(
        "/web/courts",
        params={"public_only": "invalid"},
    )

    assert response.status_code == 422


def test_excessively_long_query_is_rejected():
    response = client.get(
        "/web/courts",
        params={"q": "a" * 101},
    )

    assert response.status_code == 422


def test_directory_has_search_form():
    response = client.get("/web/courts")

    assert response.status_code == 200
    assert 'name="q"' in response.text
    assert 'name="public_only"' in response.text