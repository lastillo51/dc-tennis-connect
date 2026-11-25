"""Unit tests for DC Tennis Connect Alembic migrations."""

from pathlib import Path

from alembic.config import Config
from alembic.script import ScriptDirectory


PROJECT_ROOT = Path(__file__).resolve().parents[3]

INITIAL_REVISION = "70a0a04f5a58"
SOURCE_IDENTIFIER_REVISION = "b83f1c2d9a60"
EXPECTED_REVISION = "61174a56cf41"


def get_script_directory():
    config = Config(str(PROJECT_ROOT / "alembic.ini"))
    return ScriptDirectory.from_config(config)


def test_alembic_configuration_exists():
    assert (PROJECT_ROOT / "alembic.ini").is_file()
    assert (PROJECT_ROOT / "alembic" / "env.py").is_file()


def test_initial_migration_exists():
    script = get_script_directory()

    assert script.get_revision(INITIAL_REVISION) is not None


def test_initial_migration_has_no_parent():
    script = get_script_directory()

    revision = script.get_revision(INITIAL_REVISION)

    assert revision.down_revision is None


def test_source_identifier_migration_has_correct_parent():
    script = get_script_directory()

    revision = script.get_revision(
        SOURCE_IDENTIFIER_REVISION
    )

    assert revision is not None
    assert revision.down_revision == INITIAL_REVISION


def test_nullable_reservation_migration_has_correct_parent():
    script = get_script_directory()

    revision = script.get_revision(EXPECTED_REVISION)

    assert revision is not None
    assert revision.down_revision == SOURCE_IDENTIFIER_REVISION


def test_expected_revision_is_current_head():
    script = get_script_directory()

    assert script.get_current_head() == EXPECTED_REVISION
    assert script.get_heads() == [EXPECTED_REVISION]


def test_all_migrations_have_upgrade_and_downgrade():
    script = get_script_directory()

    for revision_id in (
        INITIAL_REVISION,
        SOURCE_IDENTIFIER_REVISION,
        EXPECTED_REVISION,
    ):
        revision = script.get_revision(revision_id)

        assert callable(revision.module.upgrade)
        assert callable(revision.module.downgrade)


def test_migration_files_are_in_versions_directory():
    script = get_script_directory()

    for revision_id in (
        INITIAL_REVISION,
        SOURCE_IDENTIFIER_REVISION,
        EXPECTED_REVISION,
    ):
        revision = script.get_revision(revision_id)
        path = Path(revision.path)

        assert path.parent.name == "versions"
        assert path.suffix == ".py"