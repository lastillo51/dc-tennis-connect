"""Shared database fixtures for DC Tennis Connect tests."""

import os

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session



TEST_DATABASE_NAME = "dc_tennis_test"


@pytest.fixture(scope="session")
def test_engine():
    """Connect only to the dedicated PostgreSQL test database."""

    if os.getenv("RUN_DB_TESTS") != "1":
        pytest.skip("Database integration tests are disabled")

    # Import only after database tests are explicitly enabled.
    from app.db.session import get_database_url

    url = get_database_url().set(
        database="dc_tennis_test"
    )

    if url.database != "dc_tennis_test":
        raise RuntimeError(
            "Refusing to use a non-test database"
        )

    engine = create_engine(
        url,
        pool_pre_ping=True,
    )

    try:
        yield engine
    finally:
        engine.dispose()


@pytest.fixture
def db_session(test_engine):
    """Provide a session whose changes are rolled back."""

    with test_engine.connect() as connection:
        transaction = connection.begin()

        with Session(
            bind=connection,
            join_transaction_mode="create_savepoint",
        ) as session:
            yield session

        transaction.rollback()


@pytest.fixture
def court_test_data(db_session):
    """Seed fictional courts and override FastAPI's database dependency."""

    from app.main import app
    from app.db.session import get_db
    from app.tests.fixtures.courts import seed_sample_courts

    if get_db in app.dependency_overrides:
        raise RuntimeError(
            "get_db already has a dependency override"
        )

    seed_sample_courts(db_session)

    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    try:
        yield db_session
    finally:
        app.dependency_overrides.pop(get_db, None)