"""Unit tests for the read-only court import planner."""

from uuid import UUID

from app.importers.planner import (
    ExistingCourt,
    ImportAction,
    plan_import,
)
from app.importers.schemas import DPRCourtCandidate


def candidate(
    source_identifier="DPR_0713",
    name="Fort Davis",
    public_access=True,
    active=True,
):
    return DPRCourtCandidate(
        source_identifier=source_identifier,
        global_id=UUID("74aabf55-2ce8-424b-b493-64756814db8f"),
        object_id=239,
        name=name,
        address="41st St., Washington, DC",
        number_of_courts=1,
        active=active,
        public_access=public_access,
    )


def test_new_approved_court_is_insert():
    plans = plan_import([candidate()], {})

    assert plans[0].action == ImportAction.INSERT


def test_unverified_public_access_requires_review():
    plans = plan_import(
        [candidate(public_access=None)],
        {},
    )

    assert plans[0].action == ImportAction.REVIEW


def test_unknown_active_status_requires_review():
    plans = plan_import(
        [candidate(active=None)],
        {},
    )

    assert plans[0].action == ImportAction.REVIEW


def test_existing_unchanged_court():
    current = ExistingCourt(
        source_identifier="DPR_0713",
        name="Fort Davis",
        address="41st St., Washington, DC",
        number_of_courts=1,
    )

    plans = plan_import(
        [candidate()],
        {"DPR_0713": current},
    )

    assert plans[0].action == ImportAction.UNCHANGED


def test_existing_changed_court():
    current = ExistingCourt(
        source_identifier="DPR_0713",
        name="Previous Name",
        address="41st St., Washington, DC",
        number_of_courts=1,
    )

    plans = plan_import(
        [candidate()],
        {"DPR_0713": current},
    )

    assert plans[0].action == ImportAction.REVIEW


def test_duplicate_identity_requires_review():
    plans = plan_import(
        [candidate(), candidate()],
        {},
    )

    assert plans[0].action == ImportAction.INSERT
    assert plans[1].action == ImportAction.REVIEW