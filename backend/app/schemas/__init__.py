"""Экспорт Pydantic-схем."""

from app.schemas.vacancy import (
    VacancyCandidateRead,
    VacancyListItem,
    VacancyListResponse,
    VacancyRefreshResponse,
)
from app.schemas.university import UniversityCreate, UniversityRead

__all__ = (
    "VacancyCandidateRead",
    "VacancyListItem",
    "VacancyListResponse",
    "VacancyRefreshResponse",
    "UniversityCreate",
    "UniversityRead",
)
