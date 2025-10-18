"""Модели SQLAlchemy, связанные с вакансиями."""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, List

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.candidate import VacancyCandidate


class Vacancy(Base):
    """Описание сущности вакансии."""

    __tablename__ = "vacancy"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(254), nullable=False)
    company: Mapped[str] = mapped_column(String(254), nullable=False)
    field_file: Mapped[str] = mapped_column(String(254), nullable=False)
    platform: Mapped[str] = mapped_column(String(254), nullable=False)
    specialization: Mapped[str] = mapped_column(String(254), nullable=False)
    type_work: Mapped[str | None] = mapped_column(String(254))
    grafic: Mapped[str | None] = mapped_column(String(254))
    place_work: Mapped[str | None] = mapped_column(String(254))
    map_link: Mapped[str | None] = mapped_column(String(254))
    time: Mapped[int | None] = mapped_column(Integer)
    price: Mapped[str | None] = mapped_column(String(50))
    additionally: Mapped[str | None] = mapped_column(String(500))
    text: Mapped[str | None] = mapped_column(String(500))
    site_link: Mapped[str | None] = mapped_column(String(50))
    video_link: Mapped[str | None] = mapped_column(String(50))
    personal_data: Mapped[bool | None] = mapped_column(Boolean)
    emails_data: Mapped[bool | None] = mapped_column(Boolean)
    sms: Mapped[bool | None] = mapped_column(Boolean)
    creation_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    expiry_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    is_approved: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False, server_default="false"
    )

    responsibilities: Mapped[List["Responsibility"]] = relationship(
        back_populates="vacancy", cascade="all, delete-orphan"
    )
    conditions: Mapped[List["Condition"]] = relationship(
        back_populates="vacancy", cascade="all, delete-orphan"
    )
    candidates: Mapped[List["VacancyCandidate"]] = relationship(
        back_populates="vacancy", cascade="all, delete-orphan"
    )


class Responsibility(Base):
    """Задача или обязанность, связанная с вакансией."""

    __tablename__ = "responsibilities_list"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    vacancy_id: Mapped[int] = mapped_column(
        ForeignKey("vacancy.id", ondelete="CASCADE"), nullable=False
    )
    description: Mapped[str] = mapped_column(String(500), nullable=False)

    vacancy: Mapped["Vacancy"] = relationship(back_populates="responsibilities")


class Condition(Base):
    """Условие, относящееся к конкретной вакансии."""

    __tablename__ = "conditions_list"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    vacancy_id: Mapped[int] = mapped_column(
        ForeignKey("vacancy.id", ondelete="CASCADE"), nullable=False
    )
    description: Mapped[str] = mapped_column(String(500), nullable=False)

    vacancy: Mapped["Vacancy"] = relationship(back_populates="conditions")
