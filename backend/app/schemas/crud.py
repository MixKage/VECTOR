from __future__ import annotations
from pydantic import BaseModel, Field
from typing import Optional

# --- Простые схемы CRUD для сущностей ---

class RegionIn(BaseModel):
    """Схема для ввода данных о регионе."""
    title: str = Field(..., max_length=254)

class RegionOut(RegionIn):
    """Схема для вывода данных о регионе с идентификатором."""
    id: int

class CityIn(BaseModel):
    """Схема для ввода данных о городе."""
    region_id: Optional[int] = None  # Идентификатор региона (необязательный)
    title: str = Field(..., max_length=254)

class CityOut(CityIn):
    """Схема для вывода данных о городе с идентификатором."""
    id: int

class SpecializationIn(BaseModel):
    """Схема для ввода данных о специализации."""
    title: str = Field(..., max_length=254)  # Название специализации
    specialization_code: str = Field(..., max_length=254)  # Код специализации

class SpecializationOut(SpecializationIn):
    """Схема для вывода данных о specialization с идентификатором."""
    id: int

class UniversityIn(BaseModel):
    """Схема для ввода данных о университете."""
    account_id: Optional[int] = None  # Идентификатор учётной записи (необязательный)
    title: str = Field(..., max_length=254)  # Название университета
    city_id: Optional[int] = None  # Идентификатор города (необязательный)

class UniversityOut(UniversityIn):
    """Схема для вывода данных о университете с идентификатором."""
    id: int

class CompanyIn(BaseModel):
    """Схема для ввода данных о компании."""
    account_id: Optional[int] = None  # Идентификатор учётной записи (необязательный)
    title: str = Field(..., max_length=254)  # Название компании
    city_id: int  # Идентификатор города

class CompanyOut(CompanyIn):
    """Схема для вывода данных о компании с идентификатором."""
    id: int
