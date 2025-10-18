"""Экспорт Pydantic-схем."""

from app.schemas.stats import CompanyStat, SpecializationStat, StatsResponse
from app.schemas.university import (
    UniversityCreate,
    UniversityRead,
    UniversityRecent,
    UniversityRecentResponse,
)
from app.schemas.vacancy import (
    VacancyCandidateRead,
    VacancyListItem,
    VacancyListResponse,
    VacancyRefreshResponse,
)

__all__ = (
    "StatsResponse",
    "SpecializationStat",
    "CompanyStat",
    "UniversityCreate",
    "UniversityRead",
    "UniversityRecent",
    "UniversityRecentResponse",
    "VacancyCandidateRead",
    "VacancyListItem",
    "VacancyListResponse",
    "VacancyRefreshResponse",
)
