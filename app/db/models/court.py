"""Persistent tennis court model."""

from datetime import datetime

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Court(Base):
    __tablename__ = "courts"

    __table_args__ = (
        CheckConstraint(
            "number_of_courts >= 1",
            name="ck_courts_number_positive",
        ),
        CheckConstraint(
            "latitude BETWEEN -90 AND 90",
            name="ck_courts_latitude_range",
        ),
        CheckConstraint(
            "longitude BETWEEN -180 AND 180",
            name="ck_courts_longitude_range",
        ),
        CheckConstraint(
            "availability_status IN "
            "('published_hours', 'reservable', "
            "'first_come_first_served', 'closed', 'unknown')",
            name="ck_courts_availability_status",
        ),
    )

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    address: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    latitude: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    longitude: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    number_of_courts: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    public_access: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
    )

    availability_status: Mapped[str] = mapped_column(
        String(40),
        nullable=False,
        default="unknown",
        server_default="unknown",
    )

    reservation_required: Mapped[bool | None] = mapped_column(
        Boolean,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    sources: Mapped[list["CourtSource"]] = relationship(
        back_populates="court",
        cascade="all, delete-orphan",
    )


class CourtSource(Base):
    __tablename__ = "court_sources"

    __table_args__ = (
        CheckConstraint(
            "source_type IN "
            "('official', 'open_data', 'reservation_platform', 'other')",
            name="ck_court_sources_type",
        ),
        UniqueConstraint(
            "source_name",
            "source_identifier",
            name="uq_court_sources_source_identity",
        ),
    )

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    court_id: Mapped[int] = mapped_column(
        ForeignKey("courts.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    source_name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    source_identifier: Mapped[str | None] = mapped_column(
        String(200),
        nullable=True,
    )

    source_url: Mapped[str] = mapped_column(
        String(1000),
        nullable=False,
    )

    source_type: Mapped[str] = mapped_column(
        String(40),
        nullable=False,
    )

    last_verified_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    court: Mapped["Court"] = relationship(
        back_populates="sources",
    )