"""Unit tests for the read-only DPR import CLI."""

import json
from pathlib import Path

import pytest

from scripts.import_public_courts import (
    build_parser,
    main,
    run_dry_run,
)


def test_dry_run_is_default():
    args = build_parser().parse_args([])

    assert args.dry_run is False


def test_explicit_dry_run_is_accepted():
    args = build_parser().parse_args(["--dry-run"])

    assert args.dry_run is True


def test_apply_option_is_not_supported():
    with pytest.raises(SystemExit) as exc:
        build_parser().parse_args(["--apply"])

    assert exc.value.code == 2


def test_missing_source_is_rejected(tmp_path):
    missing = tmp_path / "missing.json"

    assert run_dry_run(missing) == 1


def test_invalid_source_is_rejected(tmp_path):
    source = tmp_path / "invalid.json"
    source.write_text(
        json.dumps({"error": {"code": 400}}),
        encoding="utf-8",
    )

    assert run_dry_run(source) == 1


def test_empty_source_is_rejected(tmp_path):
    source = tmp_path / "empty.json"
    source.write_text(
        json.dumps({"features": []}),
        encoding="utf-8",
    )

    assert run_dry_run(source) == 1


def test_cli_accepts_custom_source_path(tmp_path):
    source = tmp_path / "missing.json"

    result = main([
        "--dry-run",
        "--source",
        str(source),
    ])

    assert result == 1