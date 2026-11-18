"""Integration tests for PostgreSQL schema constraints."""

import os

import pytest
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError

pytestmark = pytest.mark.skipif(
    os.getenv("RUN_DB_TESTS") != "1",
    reason="Set RUN_DB_TESTS=1 to enable database tests",
)


@pytest.fixture
def connection():
    from app.db.session import engine

    with engine.connect() as conn:
        transaction = conn.begin()

        try:
            yield conn
        finally:
            transaction.rollback()


def test_courts_table_exists(connection):
    result = connection.execute(
        text("SELECT to_regclass('public.courts')")
    ).scalar_one()

    assert result == "courts"


def test_court_sources_table_exists(connection):
    result = connection.execute(
        text("SELECT to_regclass('public.court_sources')")
    ).scalar_one()

    assert result == "court_sources"


def test_invalid_court_count_rejected(connection):
    with pytest.raises(IntegrityError):
        connection.execute(
            text("""
                INSERT INTO courts
                    (id, name, address,
                     number_of_courts, public_access)
                VALUES
                    (-100, 'Invalid Court', 'Test Address',
                     0, true)
            """)
        )


def test_invalid_latitude_rejected(connection):
    with pytest.raises(IntegrityError):
        connection.execute(
            text("""
                INSERT INTO courts
                    (id, name, address, latitude,
                     number_of_courts, public_access)
                VALUES
                    (-101, 'Invalid Latitude', 'Test Address',
                     100, 1, true)
            """)
        )


def test_orphan_source_rejected(connection):
    with pytest.raises(IntegrityError):
        connection.execute(
            text("""
                INSERT INTO court_sources
                    (id, court_id, source_name,
                     source_url, source_type)
                VALUES
                    (-100, -999999,
                     'Test Source',
                     'https://example.org',
                     'official')
            """)
        )