"""Unit tests for DC GIS source normalization."""

import json

import pytest

from app.importers.dcgis_adapter import (
    load_dpr_candidates,
    normalize_dpr_record,
)


@pytest.fixture
def fort_davis():
    return {
        "PROPID": "DPR_0713",
        "GLOBALID": "{74AABF55-2CE8-424B-B493-64756814DB8F}",
        "OBJECTID": 239,
        "NAME": "Fort Davis",
        "ADDRESS": (
            "41st St., between Fort Davis St. "
            "& Fort Davis Pl., SE"
        ),
        "TENNISCT": 1,
        "ACTIVE": "Y",
        "USE_TYPE": "REC CENTER GROUNDS",
        "EDITED": None,
    }


def test_valid_fort_davis_record(fort_davis):
    record = normalize_dpr_record(fort_davis)

    assert record.source_identifier == "DPR_0713"
    assert record.name == "Fort Davis"
    assert record.number_of_courts == 1
    assert record.active is True
    assert record.public_access is None
    assert record.reservation_required is None


def test_missing_active_status_is_preserved(fort_davis):
    fort_davis["ACTIVE"] = None

    record = normalize_dpr_record(fort_davis)

    assert record.active is None
    assert record.requires_review


def test_zero_courts_rejected(fort_davis):
    fort_davis["TENNISCT"] = 0

    with pytest.raises(ValueError):
        normalize_dpr_record(fort_davis)


def test_missing_property_id_rejected(fort_davis):
    fort_davis["PROPID"] = None

    with pytest.raises(ValueError):
        normalize_dpr_record(fort_davis)


def test_unknown_active_classification_rejected(fort_davis):
    fort_davis["ACTIVE"] = "INVALID"

    with pytest.raises(ValueError):
        normalize_dpr_record(fort_davis)


def test_duplicate_property_rejected(tmp_path, fort_davis):
    payload = {
        "features": [
            {"attributes": fort_davis},
            {"attributes": dict(fort_davis)},
        ]
    }

    path = tmp_path / "duplicate.json"
    path.write_text(json.dumps(payload), encoding="utf-8")

    result = load_dpr_candidates(path)

    assert len(result["valid"]) == 1
    assert len(result["rejected"]) == 1


def test_arcgis_error_response_rejected(tmp_path):
    path = tmp_path / "error.json"
    path.write_text(
        json.dumps({"error": {"code": 400}}),
        encoding="utf-8",
    )

    with pytest.raises(ValueError):
        load_dpr_candidates(path)