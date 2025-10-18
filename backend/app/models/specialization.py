"""Модель соответствия специализации и направления обучения."""

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class SpecializationMapping(Base):
    """Связка между специализацией и кодом направления обучения."""

    __tablename__ = "specialization_maping"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    specialization: Mapped[str] = mapped_column(String(254), nullable=False)
    direction_of_study_code: Mapped[str] = mapped_column(String(30), nullable=False)
