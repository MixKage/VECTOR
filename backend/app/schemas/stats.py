"""Pydantic-схемы для агрегированных метрик по вакансиям."""

from typing import List

from pydantic import BaseModel, Field


class SpecializationStat(BaseModel):
    """Статистика по специальности и количеству откликов."""

    specialization: str
    applications: int = Field(..., ge=0)


class CompanyStat(BaseModel):
    """Статистика по компании: вакансии, отклики, трудоустройства."""

    company: str
    vacancies: int = Field(..., ge=0)
    total_applications: int = Field(..., ge=0)
    approved_applications: int = Field(..., ge=0)


class StatsResponse(BaseModel):
    """Сводные данные для фронтенда."""

    total_vacancies: int = Field(..., ge=0, description="Общее количество вакансий")
    total_applications: int = Field(
        ...,
        ge=0,
        description="Общее количество откликов на вакансии",
    )
    employment_rate: float = Field(
        ...,
        ge=0.0,
        le=100.0,
        description="Уровень трудоустройства (доля одобренных откликов, %)",
    )
    active_vacancies: int = Field(..., ge=0, description="Активные вакансии")
    completed_vacancies: int = Field(..., ge=0, description="Завершённые вакансии")
    moderation_vacancies: int = Field(..., ge=0, description="Вакансии на модерации")
    top_specializations: List[SpecializationStat]
    top_companies: List[CompanyStat]
