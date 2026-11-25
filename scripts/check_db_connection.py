"""Verify DC Tennis Connect PostgreSQL connectivity."""

from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from app.db.session import get_engine


def check_database_connection() -> bool:
    """Execute read-only PostgreSQL connectivity checks."""

    try:
        # Initialize the engine only when the diagnostic runs.
        engine = get_engine()

        with engine.connect() as connection:
            result = connection.execute(
                text(
                    """
                    SELECT
                        current_database() AS database_name,
                        current_user AS database_user,
                        current_setting('server_version') AS version
                    """
                )
            ).mappings().one()

            health = connection.execute(
                text("SELECT 1")
            ).scalar_one()

        if health != 1:
            print(
                "FAIL: Database health query returned "
                "an unexpected result"
            )
            return False

        print("PASS: PostgreSQL connection successful")
        print("PASS: SELECT 1 verification")
        print("Database:", result["database_name"])
        print("Database user:", result["database_user"])
        print("PostgreSQL version:", result["version"])

        return True

    except (SQLAlchemyError, RuntimeError) as exc:
        # Avoid printing the full exception because it may
        # contain connection details or sensitive information.
        print(
            "FAIL: PostgreSQL connection could not be established"
        )
        print("Error category:", type(exc).__name__)

        return False


def main() -> int:
    """Run the diagnostic and return an appropriate exit code."""

    return 0 if check_database_connection() else 1


if __name__ == "__main__":
    raise SystemExit(main())