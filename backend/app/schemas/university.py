"""Pydantic-схемы для работы с данными университетов."""

from datetime import datetime

from pydantic import BaseModel, Field


class UniversityCreate(BaseModel):
    """Данные о наборе студентов на стажировку от университета."""

    university_name: str = Field(..., description="Название университета")
    direction_of_study_code: str = Field(
        ...,
        description="Код направления подготовки",
    )
    start_date: datetime = Field(..., description="Дата начала стажировки")
    end_time: datetime = Field(..., description="Дата окончания стажировки")
    count: int = Field(..., gt=0, description="Общее количество мест")


class UniversityRead(UniversityCreate):
    """Ответ после сохранения информации об университете."""

    id: int
    reserved: int

    class Config:
        orm_mode = True

