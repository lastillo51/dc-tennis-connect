from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_homepage_returns_html():
    response = client.get("/web")

    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]


def test_homepage_contains_project_name():
    response = client.get("/web")

    assert "DC Tennis Connect" in response.text


def test_homepage_contains_court_disclaimer():
    response = client.get("/web")

    assert "does not independently" in response.text


def test_homepage_links_to_court_directory():
    response = client.get("/web")

    assert 'href="/web/courts"' in response.text


def test_static_stylesheet_is_available():
    response = client.get("/static/css/styles.css")

    assert response.status_code == 200
    assert "text/css" in response.headers["content-type"]