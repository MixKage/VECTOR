"""ЭКСПОРТ"""

from app.models.candidate import Candidate, VacancyCandidate
from app.models.intern import Intern
from app.models.specialization import SpecializationMapping
from app.models.vacancy import Condition, Responsibility, Vacancy

__all__ = (
    "Candidate",
    "VacancyCandidate",
    "Intern",
    "SpecializationMapping",
    "Condition",
    "Responsibility",
    "Vacancy",
)
