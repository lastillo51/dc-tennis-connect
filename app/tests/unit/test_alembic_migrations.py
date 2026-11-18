"""Unit tests for Alembic migration configuration."""

from pathlib import Path

from alembic.config import Config
from alembic.script import ScriptDirectory


PROJECT_ROOT = Path(__file__).resolve().parents[3]

EXPECTED_REVISION = "70a0a04f5a58"


def get_script_directory():
    config = Config(str(PROJECT_ROOT / "alembic.ini"))

    return ScriptDirectory.from_config(config)


def test_alembic_configuration_exists():
    assert (PROJECT_ROOT / "alembic.ini").is_file()
    assert (PROJECT_ROOT / "alembic" / "env.py").is_file()


def test_initial_migration_exists():
    script = get_script_directory()

    revision = script.get_revision(EXPECTED_REVISION)

    assert revision is not None


def test_initial_migration_has_no_parent():
    script = get_script_directory()

    revision = script.get_revision(EXPECTED_REVISION)

    assert revision.down_revision is None


def test_expected_revision_is_current_head():
    script = get_script_directory()

    assert script.get_current_head() == EXPECTED_REVISION


def test_migration_has_upgrade_and_downgrade():
    script = get_script_directory()

    revision = script.get_revision(EXPECTED_REVISION)

    assert callable(revision.module.upgrade)
    assert callable(revision.module.downgrade)


def test_migration_file_is_in_versions_directory():
    script = get_script_directory()

    revision = script.get_revision(EXPECTED_REVISION)

    path = Path(revision.path)

    assert path.parent.name == "versions"
    assert path.suffix == ".py"