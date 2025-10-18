"""Pydantic-схемы, описывающие структуры данных для API вакансий."""

from datetime import datetime
from typing import List

from pydantic import BaseModel


class VacancyCandidateRead(BaseModel):
    """Статус кандидата в рамках вакансии."""

    candidate_id: int
    is_new: bool
    is_approved: bool

    class Config:
        orm_mode = True


class VacancyListItem(BaseModel):
    """Данные вакансии, возвращаемые в списке."""

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
    """Обёртка ответа при выдаче списка вакансий."""

    vacancies: List[VacancyListItem]


class VacancyRefreshResponse(BaseModel):
    """Ответ после продления срока действия вакансии."""

    vacancy_id: int
    company: str
    old_expiry_date: datetime
    new_expiry_date: datetime
