"""PostgreSQL connectivity integration tests."""

import os
from pathlib import Path

import pytest
from dotenv import load_dotenv
from sqlalchemy import text

# Load local configuration explicitly, avoiding find_dotenv()
# failures with Python 3.14 and stdin-based execution.
PROJECT_ROOT = Path(__file__).resolve().parents[3]
load_dotenv(
    dotenv_path=PROJECT_ROOT / ".env",
    override=False,
)

# Database tests are opt-in so ordinary CI does not
# require a running PostgreSQL service.
RUN_DB_TESTS = os.getenv("RUN_DB_TESTS") == "1"

pytestmark = pytest.mark.skipif(
    not RUN_DB_TESTS,
    reason="Set RUN_DB_TESTS=1 to enable PostgreSQL integration tests",
)


@pytest.fixture(scope="module")
def db_components():
    """Import database components only for enabled tests."""

    from app.db.session import (
        SessionLocal,
        engine,
        get_db,
    )

    yield engine, SessionLocal, get_db

    engine.dispose()


def test_database_engine_connection(db_components):
    """Verify SQLAlchemy engine connectivity."""

    engine, _, _ = db_components

    with engine.connect() as connection:
        result = connection.execute(
            text("SELECT 1")
        ).scalar_one()

    assert result == 1


def test_database_session_connection(db_components):
    """Verify SessionLocal can execute a query."""

    _, SessionLocal, _ = db_components

    with SessionLocal() as session:
        result = session.execute(
            text("SELECT 1")
        ).scalar_one()

    assert result == 1


def test_database_dependency_connection(db_components):
    """Verify get_db provides a working session."""

    _, _, get_db = db_components

    dependency = get_db()

    try:
        session = next(dependency)

        result = session.execute(
            text("SELECT 1")
        ).scalar_one()

        assert result == 1

    finally:
        dependency.close()


def test_database_identity(db_components):
    """Verify connection to the expected PostgreSQL database."""

    engine, _, _ = db_components

    with engine.connect() as connection:
        database_name = connection.execute(
            text("SELECT current_database()")
        ).scalar_one()

        database_user = connection.execute(
            text("SELECT current_user")
        ).scalar_one()

    assert database_name == os.environ["DB_NAME"]
    assert database_user == os.environ["DB_USER"]