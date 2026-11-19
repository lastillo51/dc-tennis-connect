"""Court service integration tests."""

import os

import pytest

from app.api.schemas.court import Court
from app.api.services.court_service import (
    get_all_courts,
    get_court_by_id,
    search_courts,
)
from app.tests.fixtures.courts import seed_sample_courts


pytestmark = pytest.mark.skipif(
    os.getenv("RUN_DB_TESTS") != "1",
    reason="Set RUN_DB_TESTS=1 for PostgreSQL tests",
)


@pytest.fixture
def seeded_db(db_session):
    seed_sample_courts(db_session)
    return db_session


def test_service_returns_pydantic_courts(seeded_db):
    courts = get_all_courts(seeded_db)

    assert len(courts) == 3
    assert all(isinstance(court, Court) for court in courts)


def test_service_preserves_nested_location(seeded_db):
    court = get_court_by_id(seeded_db, 1)

    assert court is not None
    assert court.location.address == (
        "Example Address A, Washington, DC"
    )


def test_service_public_filter(seeded_db):
    courts = get_all_courts(
        seeded_db,
        public_only=True,
    )

    assert len(courts) == 2
    assert all(court.public_access for court in courts)


def test_service_missing_court(seeded_db):
    assert get_court_by_id(seeded_db, 999999) is None


def test_service_search(seeded_db):
    courts = search_courts(
        seeded_db,
        query="Sample Court A",
    )

    assert len(courts) == 1
    assert courts[0].name == "Sample Court A"