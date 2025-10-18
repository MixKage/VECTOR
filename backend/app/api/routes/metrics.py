"""Маршруты, предоставляющие агрегированную статистику для фронтенда."""

from __future__ import annotations

import logging
from datetime import datetime, timezone

from fastapi import APIRouter, Depends
from sqlalchemy import case, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.redis import get_cache, set_cache
from app.db.session import get_db
from app.models import Vacancy, VacancyCandidate
from app.schemas import CompanyStat, SpecializationStat, StatsResponse

router = APIRouter()
logger = logging.getLogger(__name__)

METRICS_CACHE_KEY = "metrics:summary"
METRICS_TTL_SECONDS = 60


@router.get("/summary", response_model=StatsResponse)
async def get_metrics_summary(db: AsyncSession = Depends(get_db)) -> StatsResponse:
    """Вернуть предобработанные метрики для фронтенда."""
    try:
        cached = await get_cache(METRICS_CACHE_KEY)
    except Exception as exc:  # noqa: BLE001
        logger.warning("Не удалось прочитать кэш метрик: %s", exc)
        cached = None

    if cached:
        return StatsResponse(**cached)

    now = datetime.now(timezone.utc)

    total_vacancies = (
        await db.execute(select(func.count(Vacancy.id)))
    ).scalar_one()

    active_vacancies = (
        await db.execute(
            select(func.count(Vacancy.id)).where(
                Vacancy.expiry_date > now,
                Vacancy.is_approved.is_(True),
            )
        )
    ).scalar_one()

    completed_vacancies = (
        await db.execute(
            select(func.count(Vacancy.id)).where(
                Vacancy.expiry_date <= now,
                Vacancy.is_approved.is_(True),
            )
        )
    ).scalar_one()

    moderation_vacancies = (
        await db.execute(
            select(func.count(Vacancy.id)).where(Vacancy.is_approved.is_(False))
        )
    ).scalar_one()

    total_applications = (
        await db.execute(select(func.count(VacancyCandidate.id)))
    ).scalar_one()

    approved_applications = (
        await db.execute(
            select(func.count(VacancyCandidate.id)).where(
                VacancyCandidate.is_approved.is_(True)
            )
        )
    ).scalar_one()

    employment_rate = (
        float(approved_applications) / float(total_applications) * 100
        if total_applications
        else 0.0
    )

    # Топ-10 специальностей
    specialization_rows = (
        await db.execute(
            select(
                Vacancy.specialization,
                func.count(VacancyCandidate.id).label("applications"),
            )
            .outerjoin(
                VacancyCandidate,
                VacancyCandidate.vacancy_id == Vacancy.id,
            )
            .group_by(Vacancy.specialization)
            .order_by(func.count(VacancyCandidate.id).desc())
            .limit(10)
        )
    ).all()
    top_specializations = [
        SpecializationStat(
            specialization=row.specialization,
            applications=row.applications,
        )
        for row in specialization_rows
    ]

    # Топ-10 компаний по числу трудоустройств (одобренных откликов)
    approved_case = case((VacancyCandidate.is_approved.is_(True), 1), else_=0)
    company_rows = (
        await db.execute(
            select(
                Vacancy.company.label("company"),
                func.count(Vacancy.id).label("vacancies"),
                func.count(VacancyCandidate.id).label("applications"),
                func.coalesce(func.sum(approved_case), 0).label("approved"),
            )
            .outerjoin(
                VacancyCandidate,
                VacancyCandidate.vacancy_id == Vacancy.id,
            )
            .group_by(Vacancy.company)
            .order_by(func.coalesce(func.sum(approved_case), 0).desc())
            .limit(10)
        )
    ).all()
    top_companies = [
        CompanyStat(
            company=row.company,
            vacancies=row.vacancies,
            total_applications=row.applications,
            approved_applications=row.approved,
        )
        for row in company_rows
    ]

    response = StatsResponse(
        total_vacancies=total_vacancies,
        total_applications=total_applications,
        employment_rate=round(employment_rate, 2),
        active_vacancies=active_vacancies,
        completed_vacancies=completed_vacancies,
        moderation_vacancies=moderation_vacancies,
        top_specializations=top_specializations,
        top_companies=top_companies,
    )

    try:
        await set_cache(
            METRICS_CACHE_KEY,
            response.dict(),
            expire_seconds=METRICS_TTL_SECONDS,
        )
    except Exception as exc:  # noqa: BLE001
        logger.warning("Не удалось записать кэш метрик: %s", exc)

    return response
