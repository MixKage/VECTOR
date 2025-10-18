"""Pydantic-схемы для данных от университетов."""

from datetime import datetime
from typing import List

from pydantic import BaseModel, Field


class UniversityCreate(BaseModel):
    """Пакет данных, который присылает университет."""

    university_name: str = Field(..., description="Название университета")
    direction_of_study_code: str = Field(
        ...,
        description="Код направления подготовки",
    )
    start_date: datetime = Field(..., description="Дата начала стажировки")
    end_time: datetime = Field(..., description="Дата окончания стажировки")
    count: int = Field(..., gt=0, description="Количество мест")


class UniversityRead(UniversityCreate):
    """Ответ после регистрации данных университета."""

    id: int
    reserved: int

    class Config:
        orm_mode = True


class UniversityRecent(BaseModel):
    """Схема для чтения последних заявок университетов из Redis."""

    university_name: str
    direction_of_study_code: str
    start_date: datetime
    end_time: datetime
    count: int
    submitted_at: datetime


class UniversityRecentResponse(BaseModel):
    """Ответ со списком последних заявок от университетов."""

    items: List[UniversityRecent]

