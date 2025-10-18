from __future__ import annotations

import sqlalchemy as sa
from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.session import Base
from typing import Optional, List


# ============================================================
# Таблица ролей
# ============================================================

class Role(Base):
    """Справочник ролей (0 - no_role, 1 - admin, 2 - HR, 3 - university, 4 - student)."""

    __tablename__ = "role"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    code: Mapped[int] = mapped_column(Integer, nullable=False, unique=True)
    title: Mapped[str] = mapped_column(String(64), nullable=False, unique=True)

    accounts: Mapped[list[Account]] = relationship(  # noqa: F821
        "Account",
        secondary="account_role",
        back_populates="roles",
    )


# ============================================================
# Ассоциационная таблица Account <-> Role (M2M)
# ============================================================

account_role = sa.Table(
    "account_role",
    Base.metadata,
    sa.Column("account_id", sa.Integer, sa.ForeignKey("account.id", ondelete="CASCADE"), primary_key=True),
    sa.Column("role_id", sa.Integer, sa.ForeignKey("role.id", ondelete="CASCADE"), primary_key=True),
)


# ============================================================
# Аккаунты
# ============================================================

class Account(Base):
    """Учётная запись пользователя (логин/пароль и связанные профили)."""

    __tablename__ = "account"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    login: Mapped[str] = mapped_column(String(254), nullable=False, unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(100), nullable=False)
    created_at: Mapped[DateTime | None] = mapped_column(DateTime(timezone=True), server_default=sa.text("now()"))

    # связи с ролями
    roles: Mapped[List["Role"]] = relationship(
        "Role", secondary=account_role, back_populates="accounts", lazy="joined"
    )

    student: Mapped[Optional["Student"]] = relationship("Student", back_populates="account", uselist=False)
    university: Mapped[Optional["University"]] = relationship("University", back_populates="account", uselist=False)
    company: Mapped[Optional["Company"]] = relationship("Company", back_populates="account", uselist=False)

    def roles_codes(self) -> list[int]:
        roles = self.roles or []
        codes = sorted({role.code for role in roles})
        return codes if codes else [0]


# ============================================================
# Студенты
# ============================================================

class Student(Base):
    """Профиль студента."""

    __tablename__ = "student"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    account_id: Mapped[int | None] = mapped_column(ForeignKey("account.id", ondelete="CASCADE"), unique=True)
    surname: Mapped[str] = mapped_column(String(254), nullable=False)
    name: Mapped[str] = mapped_column(String(254), nullable=False)
    middle_name: Mapped[str] = mapped_column(String(254), nullable=False)
    birth_date: Mapped[DateTime] = mapped_column(DateTime(timezone=True), nullable=False)

    account: Mapped[Optional["Account"]] = relationship("Account", back_populates="student", uselist=False)


# ============================================================
# Регионы
# ============================================================

class Region(Base):
    """Справочник регионов."""

    __tablename__ = "region"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(254), nullable=False, unique=True)

    cities: Mapped[list[City]] = relationship(back_populates="region")  # noqa: F821


# ============================================================
# Города
# ============================================================

class City(Base):
    """Справочник городов."""

    __tablename__ = "city"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    region_id: Mapped[int | None] = mapped_column(ForeignKey("region.id", ondelete="CASCADE"))
    title: Mapped[str] = mapped_column(String(254), nullable=False)

    region: Mapped["Region | None"] = relationship(back_populates="cities")
    __table_args__ = (UniqueConstraint("region_id", "title", name="uq_city_region_title"),)


# ============================================================
# Специализации
# ============================================================

class Specialization(Base):
    """Справочник специализаций."""

    __tablename__ = "specialization"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(254), nullable=False)
    specialization_code: Mapped[str] = mapped_column(String(254), nullable=False, unique=True)


# ============================================================
# Университеты
# ============================================================

class University(Base):
    """Профиль университета."""

    __tablename__ = "university"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    account_id: Mapped[int | None] = mapped_column(ForeignKey("account.id", ondelete="CASCADE"), unique=True)
    title: Mapped[str] = mapped_column(String(254), nullable=False)
    city_id: Mapped[int | None] = mapped_column(ForeignKey("city.id", ondelete="CASCADE"))

    account: Mapped[Optional["Account"]] = relationship("Account", back_populates="university", uselist=False)
    city: Mapped["City | None"] = relationship()


# ============================================================
# Компании
# ============================================================

class Company(Base):
    """Профиль компании."""

    __tablename__ = "company"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    account_id: Mapped[int | None] = mapped_column(ForeignKey("account.id", ondelete="CASCADE"), unique=True)
    title: Mapped[str] = mapped_column(String(254), nullable=False)
    city_id: Mapped[int] = mapped_column(ForeignKey("city.id", ondelete="CASCADE"))

    account: Mapped[Optional["Account"]] = relationship("Account", back_populates="company", uselist=False)
    city: Mapped["City | None"] = relationship()


# ============================================================
# Специализации компаний
# ============================================================

class SpecializationCompany(Base):
    """Связь компания - специализация (многие ко многим через отдельную таблицу)."""

    __tablename__ = "specialization_company"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    company_id: Mapped[int] = mapped_column(ForeignKey("company.id", ondelete="CASCADE"))
    specialization_id: Mapped[int] = mapped_column(ForeignKey("specialization.id", ondelete="CASCADE"))

    __table_args__ = (UniqueConstraint("company_id", "specialization_id", name="uq_specialization_company_pair"),)


# ============================================================
# Типы взаимодействий
# ============================================================

class InteractionType(Base):
    """Тип взаимодействия компании и студента (например: стажировка, проект и т.п.)."""

    __tablename__ = "interaction_type"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    code: Mapped[str] = mapped_column(String(254), nullable=False, unique=True)
    title: Mapped[str] = mapped_column(String(254), nullable=False)


# ============================================================
# Взаимодействия компаний и студентов
# ============================================================

class Interaction(Base):
    """Запись о взаимодействии компании со студентом."""

    __tablename__ = "interaction"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("student.id", ondelete="CASCADE"))
    company_id: Mapped[int] = mapped_column(ForeignKey("company.id", ondelete="CASCADE"))
    interaction_type_id: Mapped[int] = mapped_column(ForeignKey("interaction_type.id", ondelete="CASCADE"))
    period_start: Mapped[DateTime] = mapped_column(DateTime(timezone=True), nullable=False)
    period_end: Mapped[DateTime | None] = mapped_column(DateTime(timezone=True))
    interaction_comment: Mapped[str | None] = mapped_column(String(254))

    __table_args__ = (
        sa.CheckConstraint("period_end IS NULL OR period_end >= period_start", name="ck_interaction_period"),
    )


# ============================================================
# Образовательные программы / направления
# ============================================================

class EducationalProgram(Base):
    """Образовательная программа."""

    __tablename__ = "educational_program"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    specialization_id: Mapped[int] = mapped_column(ForeignKey("specialization.id", ondelete="CASCADE"))
    university_id: Mapped[int] = mapped_column(ForeignKey("university.id", ondelete="CASCADE"))

    __table_args__ = (UniqueConstraint("specialization_id", "university_id", name="uq_program_spec_uni"),)


# ============================================================
# Образование студентов
# ============================================================

class Study(Base):
    """Информация об обучении студента в университете."""

    __tablename__ = "study"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("student.id", ondelete="CASCADE"))
    university_id: Mapped[int] = mapped_column(ForeignKey("university.id", ondelete="CASCADE"))
    period_start: Mapped[DateTime] = mapped_column(DateTime(timezone=True), nullable=False)
    period_end: Mapped[DateTime | None] = mapped_column(DateTime(timezone=True))
    educational_program_id: Mapped[int] = mapped_column(ForeignKey("educational_program.id", ondelete="CASCADE"))

    __table_args__ = (
        sa.CheckConstraint("period_end IS NULL OR period_end >= period_start", name="ck_study_period"),
    )


# ============================================================
# Дисциплины
# ============================================================

class Subject(Base):
    """Дисциплины образовательной программы."""

    __tablename__ = "subject"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(254), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    educational_program_id: Mapped[int] = mapped_column(ForeignKey("educational_program.id", ondelete="CASCADE"))


# ============================================================
# Оценки
# ============================================================

class Marks(Base):
    """Оценки студентов по дисциплинам."""

    __tablename__ = "marks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    subject_id: Mapped[int] = mapped_column(ForeignKey("subject.id", ondelete="CASCADE"))
    student_id: Mapped[int] = mapped_column(ForeignKey("student.id", ondelete="CASCADE"))
    mark: Mapped[int] = mapped_column(Integer, nullable=False)

    __table_args__ = (
        UniqueConstraint("subject_id", "student_id", name="uq_marks_subject_student"),
        sa.CheckConstraint("mark >= 0 AND mark <= 100", name="ck_marks_range"),
    )


# ============================================================
# Проекты компаний
# ============================================================

class Project(Base):
    """Проект компании."""

    __tablename__ = "project"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(254), nullable=False)
    company_id: Mapped[int] = mapped_column(ForeignKey("company.id", ondelete="CASCADE"))
    description: Mapped[str] = mapped_column(Text, nullable=False)


# ============================================================
# Требуемые кадры для проектов
# ============================================================

class RequiredStaff(Base):
    """Требуемые кадры для проектов."""

    __tablename__ = "required_staff"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(254), nullable=False)
    project_id: Mapped[int] = mapped_column(ForeignKey("project.id", ondelete="CASCADE"))
    specialization_id: Mapped[int] = mapped_column(ForeignKey("specialization.id", ondelete="CASCADE"))
