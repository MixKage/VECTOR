"""Модель для учёта стажировок."""

from datetime import datetime

from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Intern(Base):
    """Отражает доступные места на стажировке."""

    __tablename__ = "intern"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    university_name: Mapped[str] = mapped_column(String(254), nullable=False)
    direction_of_study_code: Mapped[str] = mapped_column(String(30), nullable=False)
    start_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    end_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    count: Mapped[int] = mapped_column(Integer, nullable=False)
    reserved: Mapped[int] = mapped_column(Integer, nullable=False)
