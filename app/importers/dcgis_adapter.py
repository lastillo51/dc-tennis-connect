"""Normalize DC Parks Layer 9 ArcGIS JSON records."""

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from pydantic import ValidationError

from app.importers.schemas import DPRCourtCandidate


def parse_arcgis_timestamp(value: Any) -> datetime | None:
    """Convert ArcGIS milliseconds to a UTC datetime."""

    if value is None:
        return None

    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError("Invalid ArcGIS timestamp")

    try:
        return datetime.fromtimestamp(
            value / 1000,
            tz=timezone.utc,
        )
    except (OverflowError, OSError, ValueError) as exc:
        raise ValueError("Invalid ArcGIS timestamp") from exc


def normalize_dpr_record(
    attributes: dict[str, Any],
) -> DPRCourtCandidate:
    """Normalize one DC Parks Layer 9 record."""

    if not isinstance(attributes, dict):
        raise ValueError("Expected ArcGIS attributes object")

    active_value = attributes.get("ACTIVE")

    if active_value == "Y":
        active = True
    elif active_value == "N":
        active = False
    elif active_value is None:
        active = None
    else:
        raise ValueError("Unexpected ACTIVE classification")

    court_count = attributes.get("TENNISCT")

    if type(court_count) is not int or court_count < 1:
        raise ValueError("TENNISCT must be a positive integer")

    prop_id = attributes.get("PROPID")
    if not isinstance(prop_id, str) or not prop_id.strip():
        raise ValueError("Missing valid PROPID")

    return DPRCourtCandidate(
        source_identifier=prop_id,
        global_id=attributes.get("GLOBALID"),
        object_id=attributes.get("OBJECTID"),
        name=attributes.get("NAME"),
        address=attributes.get("ADDRESS"),
        number_of_courts=court_count,
        active=active,
        use_type=attributes.get("USE_TYPE"),
        source_edited_at=parse_arcgis_timestamp(
            attributes.get("EDITED")
        ),
    )


def load_dpr_candidates(path: Path) -> dict:
    """Validate a saved ArcGIS response without database writes."""

    data = json.loads(path.read_text(encoding="utf-8"))

    if not isinstance(data, dict):
        raise ValueError("Expected ArcGIS JSON object")

    if "error" in data:
        raise ValueError("ArcGIS returned an error response")

    if data.get("exceededTransferLimit"):
        raise ValueError("ArcGIS response is incomplete")

    features = data.get("features")

    if not isinstance(features, list):
        raise ValueError("Missing ArcGIS features list")

    valid = []
    rejected = []
    seen_ids = set()

    for index, feature in enumerate(features):
        try:
            if not isinstance(feature, dict):
                raise ValueError("Invalid feature object")

            candidate = normalize_dpr_record(
                feature.get("attributes")
            )

            identity = (
                candidate.source_name,
                candidate.source_identifier,
            )

            if identity in seen_ids:
                raise ValueError("Duplicate source identity")

            seen_ids.add(identity)
            valid.append(candidate)

        except (ValueError, TypeError, ValidationError) as exc:
            rejected.append({
                "index": index,
                "reason": type(exc).__name__,
            })

    return {
        "valid": valid,
        "rejected": rejected,
        "total": len(features),
    }