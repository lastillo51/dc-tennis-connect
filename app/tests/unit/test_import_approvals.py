"""Tests for the DPR approval manifest."""

import json

import pytest

from app.importers.approvals import load_approvals


def test_empty_approval_manifest_is_valid(tmp_path):
    path = tmp_path / "approvals.json"

    path.write_text(
        json.dumps({
            "schema_version": 1,
            "source_name": "dcgis-dpr-parks",
            "approved_facilities": [],
        }),
        encoding="utf-8",
    )

    manifest = load_approvals(path)

    assert manifest.approved_facilities == []


def test_duplicate_approvals_rejected(tmp_path):
    approval = {
        "source_identifier": "DPR_0713",
        "public_access": True,
        "evidence_url": "https://example.org/public-access",
        "verified_at": "2026-11-21T20:00:00Z",
    }

    path = tmp_path / "approvals.json"

    path.write_text(
        json.dumps({
            "schema_version": 1,
            "source_name": "dcgis-dpr-parks",
            "approved_facilities": [approval, approval],
        }),
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="Duplicate"):
        load_approvals(path)


def test_unknown_public_access_cannot_be_approved(tmp_path):
    path = tmp_path / "approvals.json"

    path.write_text(
        json.dumps({
            "schema_version": 1,
            "source_name": "dcgis-dpr-parks",
            "approved_facilities": [{
                "source_identifier": "DPR_0713",
                "public_access": False,
                "evidence_url": "https://example.org/evidence",
                "verified_at": "2026-11-21T20:00:00Z",
            }],
        }),
        encoding="utf-8",
    )

    with pytest.raises(ValueError):
        load_approvals(path)