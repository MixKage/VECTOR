"""Модели SQLAlchemy, связанные с кандидатами."""

from __future__ import annotations

from typing import TYPE_CHECKING, List

from sqlalchemy import Boolean, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.vacancy import Vacancy


class Candidate(Base):
    """Описание кандидата, откликающегося на вакансии."""

    __tablename__ = "candidate"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    surname: Mapped[str] = mapped_column(String(254), nullable=False)
    name: Mapped[str] = mapped_column(String(254), nullable=False)
    middle_name: Mapped[str] = mapped_column(String(254), nullable=False)
    phone: Mapped[str] = mapped_column(String(11), nullable=False)
    email: Mapped[str] = mapped_column(String(50), nullable=False)
    cv_link: Mapped[str] = mapped_column(String(254), nullable=False)

    vacancies: Mapped[List["VacancyCandidate"]] = relationship(
        back_populates="candidate", cascade="all, delete-orphan"
    )


class VacancyCandidate(Base):
    """Связующая таблица со статусами кандидата по вакансии."""

    __tablename__ = "vacancy_candidate"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    vacancy_id: Mapped[int] = mapped_column(
        ForeignKey("vacancy.id", ondelete="CASCADE"), nullable=False
    )
    candidate_id: Mapped[int] = mapped_column(
        ForeignKey("candidate.id", ondelete="CASCADE"), nullable=False
    )
    is_new: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=True, server_default="true"
    )
    is_approved: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False, server_default="false"
    )

    vacancy: Mapped["Vacancy"] = relationship(back_populates="candidates")
    candidate: Mapped["Candidate"] = relationship(back_populates="vacancies")
