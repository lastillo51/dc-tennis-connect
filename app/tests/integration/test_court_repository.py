"""Repository integration tests using isolated PostgreSQL."""

import os

import pytest

from app.db.repositories import court_repository
from app.tests.fixtures.courts import seed_sample_courts


pytestmark = pytest.mark.skipif(
    os.getenv("RUN_DB_TESTS") != "1",
    reason="Set RUN_DB_TESTS=1 for PostgreSQL tests",
)


@pytest.fixture
def seeded_db(db_session):
    seed_sample_courts(db_session)
    return db_session


def test_repository_returns_three_courts(seeded_db):
    courts = court_repository.get_all_courts(seeded_db)

    assert len(courts) == 3


def test_repository_filters_public_courts(seeded_db):
    courts = court_repository.get_all_courts(
        seeded_db,
        public_only=True,
    )

    assert len(courts) == 2
    assert all(court.public_access for court in courts)


def test_repository_finds_court_by_id(seeded_db):
    court = court_repository.get_court_by_id(
        seeded_db,
        1,
    )

    assert court is not None
    assert court.name == "Sample Court A"


def test_repository_returns_none_for_missing_id(seeded_db):
    court = court_repository.get_court_by_id(
        seeded_db,
        999999,
    )

    assert court is None


def test_repository_searches_names(seeded_db):
    courts = court_repository.search_courts(
        seeded_db,
        query="Sample Court A",
    )

    assert len(courts) == 1
    assert courts[0].name == "Sample Court A"


def test_repository_searches_addresses(seeded_db):
    courts = court_repository.search_courts(
        seeded_db,
        query="Example Address A",
    )

    assert len(courts) == 1


@pytest.mark.parametrize("query", ["%", "_"])
def test_repository_treats_sql_wildcards_literally(
    seeded_db,
    query,
):
    courts = court_repository.search_courts(
        seeded_db,
        query=query,
    )

    assert courts == []