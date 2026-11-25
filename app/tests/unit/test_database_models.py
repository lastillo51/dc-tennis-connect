"""Unit tests for SQLAlchemy court model metadata."""

from sqlalchemy import CheckConstraint, ForeignKeyConstraint

from app.db.base import Base
from app.db.models import Court, CourtSource


def test_expected_tables_registered():
    assert set(Base.metadata.tables) == {
        "courts",
        "court_sources",
    }


def test_court_table_name():
    assert Court.__tablename__ == "courts"


def test_source_table_name():
    assert CourtSource.__tablename__ == "court_sources"


def test_source_foreign_key():
    constraints = [
        constraint
        for constraint in CourtSource.__table__.constraints
        if isinstance(constraint, ForeignKeyConstraint)
    ]

    assert any(
        element.target_fullname == "courts.id"
        for constraint in constraints
        for element in constraint.elements
    )


def test_court_constraints_present():
    names = {
        constraint.name
        for constraint in Court.__table__.constraints
        if isinstance(constraint, CheckConstraint)
    }

    assert {
        "ck_courts_number_positive",
        "ck_courts_latitude_range",
        "ck_courts_longitude_range",
        "ck_courts_availability_status",
    } <= names


def test_source_type_constraint_present():
    names = {
        constraint.name
        for constraint in CourtSource.__table__.constraints
        if isinstance(constraint, CheckConstraint)
    }

    assert "ck_court_sources_type" in names


def test_required_court_columns():
    columns = Court.__table__.columns

    assert columns["name"].nullable is False
    assert columns["address"].nullable is False
    assert columns["number_of_courts"].nullable is False
    assert columns["public_access"].nullable is False


def test_optional_coordinates():
    columns = Court.__table__.columns

    assert columns["latitude"].nullable is True
    assert columns["longitude"].nullable is True


def test_source_relationship():
    assert Court.sources.property.mapper.class_ is CourtSource
    assert CourtSource.court.property.mapper.class_ is Court