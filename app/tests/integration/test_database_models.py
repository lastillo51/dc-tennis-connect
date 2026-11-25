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
    """Provide a connection with transaction rollback cleanup."""

    from app.db.session import get_engine

    engine = get_engine()

    with engine.connect() as conn:
        transaction = conn.begin()

        try:
            yield conn
        finally:
            if transaction.is_active:
                transaction.rollback()


def test_courts_table_exists(connection):
    """Verify the courts table exists."""

    result = connection.execute(
        text("SELECT to_regclass('public.courts')")
    ).scalar_one()

    assert result == "courts"


def test_court_sources_table_exists(connection):
    """Verify the court_sources table exists."""

    result = connection.execute(
        text("SELECT to_regclass('public.court_sources')")
    ).scalar_one()

    assert result == "court_sources"


def test_invalid_court_count_rejected(connection):
    """Reject a court containing fewer than one court."""

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
    """Reject coordinates outside the valid latitude range."""

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
    """Reject source records without an existing parent court."""

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


def test_reservation_required_accepts_null(connection):
    """PostgreSQL accepts an unknown official reservation policy."""

    result = connection.execute(
        text("""
            INSERT INTO courts (
                name,
                address,
                number_of_courts,
                public_access,
                reservation_required
            )
            VALUES (
                'Fictional Nullable Policy Court',
                'Example Address, Washington, DC',
                1,
                TRUE,
                NULL
            )
            RETURNING id, reservation_required
        """)
    ).mappings().one()

    assert result["id"] > 0
    assert result["reservation_required"] is None


def test_reservation_required_has_no_server_default(connection):
    """Omitting the policy should store NULL, not FALSE."""

    result = connection.execute(
        text("""
            INSERT INTO courts (
                name,
                address,
                number_of_courts,
                public_access
            )
            VALUES (
                'Fictional Default Policy Court',
                'Example Address, Washington, DC',
                1,
                TRUE
            )
            RETURNING reservation_required
        """)
    ).scalar_one()

    assert result is None