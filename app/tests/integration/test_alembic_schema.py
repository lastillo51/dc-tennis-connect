"""Read-only PostgreSQL migration verification tests."""

import os

import pytest
from sqlalchemy import inspect, text


pytestmark = pytest.mark.skipif(
    os.getenv("RUN_DB_TESTS") != "1",
    reason="Set RUN_DB_TESTS=1 to enable database tests",
)


EXPECTED_REVISION = "61174a56cf41"


@pytest.fixture(scope="module")
def db_engine():
    """Provide the lazily initialized SQLAlchemy engine."""

    from app.db.session import get_engine

    yield get_engine()


def test_alembic_version_table_exists(db_engine):
    inspector = inspect(db_engine)

    assert "alembic_version" in inspector.get_table_names()


def test_expected_application_tables_exist(db_engine):
    inspector = inspect(db_engine)

    tables = set(inspector.get_table_names())

    assert {"courts", "court_sources"} <= tables


def test_database_revision_matches_expected(db_engine):
    with db_engine.connect() as connection:
        revision = connection.execute(
            text("SELECT version_num FROM alembic_version")
        ).scalar_one()

    assert revision == EXPECTED_REVISION


def test_court_source_foreign_key_exists(db_engine):
    inspector = inspect(db_engine)

    foreign_keys = inspector.get_foreign_keys("court_sources")

    assert any(
        key["referred_table"] == "courts"
        and key["constrained_columns"] == ["court_id"]
        for key in foreign_keys
    )


def test_database_check_constraints_exist(db_engine):
    inspector = inspect(db_engine)

    constraints = {
        constraint["name"]
        for constraint in inspector.get_check_constraints("courts")
    }

    assert {
        "ck_courts_number_positive",
        "ck_courts_latitude_range",
        "ck_courts_longitude_range",
        "ck_courts_availability_status",
    } <= constraints


def test_reservation_required_is_nullable(db_engine):
    """Verify the database permits unknown reservation policies."""

    inspector = inspect(db_engine)

    columns = {
        column["name"]: column
        for column in inspector.get_columns("courts")
    }

    assert "reservation_required" in columns
    assert columns["reservation_required"]["nullable"] is True


def test_reservation_required_has_no_default(db_engine):
    """Verify the old FALSE database default was removed."""

    inspector = inspect(db_engine)

    columns = {
        column["name"]: column
        for column in inspector.get_columns("courts")
    }

    assert columns["reservation_required"]["default"] is None