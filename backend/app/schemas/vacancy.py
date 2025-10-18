"""Pydantic-схемы для работы с вакансиями."""

from datetime import datetime
from typing import List

from pydantic import BaseModel


class VacancyCandidateRead(BaseModel):
    """Информация о кандидате, откликнувшемся на вакансию."""

    candidate_id: int
    is_new: bool
    is_approved: bool

    class Config:
        orm_mode = True


class VacancyListItem(BaseModel):
    """Короткое представление вакансии для списков."""

    id: int
    name: str
    company: str
    specialization: str
    creation_date: datetime
    expiry_date: datetime
    candidates: List[VacancyCandidateRead]

    class Config:
        orm_mode = True


class VacancyListResponse(BaseModel):
    """Ответ при запросе списка вакансий."""

    vacancies: List[VacancyListItem]


class VacancyRefreshResponse(BaseModel):
    """Ответ после продления срока действия вакансии."""

    vacancy_id: int
    company: str
    refresh_count: int
    old_expiry_date: datetime
    new_expiry_date: datetime

