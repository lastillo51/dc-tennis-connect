from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_root_endpoint():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["application"] == "DC Tennis Connect"


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_list_all_courts():
    response = client.get("/courts/")

    assert response.status_code == 200

    courts = response.json()

    assert len(courts) == 3
    assert courts[0]["name"] == "Sample Court A"


def test_filter_public_courts():
    response = client.get(
        "/courts/",
        params={"public_only": "true"},
    )

    assert response.status_code == 200

    courts = response.json()

    assert len(courts) == 2
    assert all(court["public_access"] for court in courts)


def test_get_court_by_id():
    response = client.get("/courts/1")

    assert response.status_code == 200

    court = response.json()

    assert court["id"] == 1
    assert court["name"] == "Sample Court A"
    assert court["location"]["address"] == (
        "Example Address A, Washington, DC"
    )
    assert court["google_maps_url"].startswith(
        "https://www.google.com/maps/dir/"
    )


def test_nonexistent_court():
    response = client.get("/courts/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Court not found"


def test_invalid_court_id():
    response = client.get("/courts/abc")

    assert response.status_code == 422


def test_invalid_public_only_parameter():
    response = client.get(
        "/courts/",
        params={"public_only": "invalid"},
    )

    assert response.status_code == 422
