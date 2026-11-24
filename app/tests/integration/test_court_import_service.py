"""Integration tests for the DPR court import service."""

import os
from uuid import uuid4

import pytest
from sqlalchemy import select

from app.db.models.court import CourtSource
from app.importers.schemas import DPRCourtCandidate
from app.importers.service import import_approved_courts


pytestmark = pytest.mark.skipif(
    os.getenv("RUN_DB_TESTS") != "1",
    reason="Set RUN_DB_TESTS=1 for PostgreSQL integration tests",
)


def make_candidate() -> DPRCourtCandidate:
    """Build a fictional approved court candidate."""

    return DPRCourtCandidate(
        source_identifier=f"TEST_{uuid4().hex}",
        global_id=uuid4(),
        object_id=1,
        name="Fictional Import Test Court",
        address="Example Address, Washington, DC",
        number_of_courts=2,
        active=True,
        public_access=True,
        reservation_required=None,
    )


def test_import_requires_explicit_apply(db_session):
    with pytest.raises(ValueError, match="apply=True"):
        import_approved_courts(
            db_session,
            [make_candidate()],
        )


def test_unapproved_candidate_is_rejected(db_session):
    candidate = make_candidate().model_copy(
        update={"public_access": None}
    )

    with db_session.begin():
        with pytest.raises(ValueError, match="Public access"):
            import_approved_courts(
                db_session,
                [candidate],
                apply=True,
            )

def test_duplicate_input_batch_is_rejected(db_session):
    candidate = make_candidate()

    with db_session.begin():
        with pytest.raises(ValueError, match="Duplicate identity"):
            import_approved_courts(
                db_session,
                [candidate, candidate],
                apply=True,
            )

def test_repeated_import_does_not_duplicate(db_session):
    candidate = make_candidate()

    with db_session.begin():
        first = import_approved_courts(
            db_session,
            [candidate],
            apply=True,
        )

        second = import_approved_courts(
            db_session,
            [candidate],
            apply=True,
        )

        assert first == {
            "inserted": 1,
            "unchanged": 0,
        }

        assert second == {
            "inserted": 0,
            "unchanged": 1,
        }

        sources = db_session.scalars(
            select(CourtSource).where(
                CourtSource.source_identifier
                == candidate.source_identifier
            )
        ).all()

        assert len(sources) == 1

def test_failed_batch_does_not_persist_records(db_session):
    first = make_candidate()

    second = make_candidate().model_copy(
        update={
            "source_identifier": first.source_identifier,
        }
    )

    with db_session.begin():
        with pytest.raises(ValueError, match="Duplicate identity"):
            import_approved_courts(
                db_session,
                [first, second],
                apply=True,
            )

        sources = db_session.scalars(
            select(CourtSource).where(
                CourtSource.source_identifier
                == first.source_identifier
            )
        ).all()

        assert sources == []


def test_import_rolls_back_after_database_failure(
    db_session,
    monkeypatch,
):
    """A database failure must not leave a partial import."""

    from sqlalchemy import select

    from app.db.models.court import CourtSource
    from app.importers import service

    candidate = make_candidate()

    original_flush = db_session.flush
    flush_count = 0

    def failing_flush(*args, **kwargs):
        nonlocal flush_count
        flush_count += 1

        if flush_count == 2:
            raise RuntimeError("Simulated database failure")

        return original_flush(*args, **kwargs)

    monkeypatch.setattr(
        db_session,
        "flush",
        failing_flush,
    )

    with pytest.raises(RuntimeError, match="Simulated"):
        with db_session.begin():
            service.import_approved_courts(
                db_session,
                [candidate],
                apply=True,
            )

    # Restore flush before querying.
    monkeypatch.setattr(
        db_session,
        "flush",
        original_flush,
    )

    sources = db_session.scalars(
        select(CourtSource).where(
            CourtSource.source_identifier
            == candidate.source_identifier
        )
    ).all()

    assert sources == []