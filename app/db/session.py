"""Database engine and session management for DC Tennis Connect."""

import os
from collections.abc import Generator
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import URL, create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker


BASE_DIR = Path(__file__).resolve().parents[2]
ENV_FILE = BASE_DIR / ".env"

# Explicit path avoids python-dotenv discovery issues.
# Existing environment variables take precedence.
load_dotenv(dotenv_path=ENV_FILE, override=False)


def get_database_url() -> URL:
    """Construct a database URL without manually encoding credentials."""

    required = (
        "DB_HOST",
        "DB_PORT",
        "DB_NAME",
        "DB_USER",
        "DB_PASSWORD",
    )

    missing = [
        name
        for name in required
        if not os.getenv(name)
    ]

    if missing:
        raise RuntimeError(
            "Missing database configuration: "
            + ", ".join(missing)
        )

    try:
        port = int(os.environ["DB_PORT"])
    except ValueError as exc:
        raise RuntimeError(
            "DB_PORT must be a valid integer"
        ) from exc

    if not 1 <= port <= 65535:
        raise RuntimeError(
            "DB_PORT must be between 1 and 65535"
        )

    return URL.create(
        drivername="postgresql+psycopg",
        username=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        host=os.environ["DB_HOST"],
        port=port,
        database=os.environ["DB_NAME"],
    )


def create_db_engine() -> Engine:
    """Create the SQLAlchemy engine with connection health checks."""

    return create_engine(
        get_database_url(),
        pool_pre_ping=True,
        pool_size=5,
        max_overflow=5,
        pool_timeout=30,
    )


# Engine construction does not immediately connect to PostgreSQL.
engine = create_db_engine()

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    expire_on_commit=False,
)


def get_db() -> Generator[Session, None, None]:
    """Provide a database session and always close it afterward."""

    with SessionLocal() as db:
        yield db