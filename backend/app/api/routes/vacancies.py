"""Маршруты API, связанные с вакансиями."""

from __future__ import annotations

import logging
from datetime import datetime

from dateutil.relativedelta import relativedelta
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.redis import delete_by_pattern, get_cache, set_cache
from app.db.session import get_db
from app.models import Vacancy
from app.schemas import VacancyListResponse, VacancyRefreshResponse

router = APIRouter()
logger = logging.getLogger(__name__)

VACANCY_CACHE_PREFIX = "vacancies:list"


@router.get("/", response_model=VacancyListResponse)
async def list_vacancies(
    company: str | None = Query(
        None,
        alias="filter",
        description="Фильтр по названию компании",
    ),
    db: AsyncSession = Depends(get_db),
) -> VacancyListResponse:
    """Вернуть вакансии с опциональным фильтром по названию компании."""
    cache_key = f"{VACANCY_CACHE_PREFIX}:{company or 'all'}"

    try:
        cached_payload = await get_cache(cache_key)
    except Exception as exc:  # noqa: BLE001
        logger.warning("Не удалось прочитать кэш списка вакансий: %s", exc)
        cached_payload = None

    if cached_payload:
        return VacancyListResponse(**cached_payload)

    stmt = (
        select(Vacancy)
        .options(selectinload(Vacancy.candidates))
        .order_by(Vacancy.creation_date.desc())
    )

    if company:
        stmt = stmt.where(Vacancy.company.ilike(f"%{company}%"))

    result = await db.execute(stmt)
    vacancies = result.scalars().unique().all()
    response_model = VacancyListResponse(vacancies=vacancies)

    try:
        await set_cache(cache_key, response_model.dict())
    except Exception as exc:  # noqa: BLE001
        logger.warning("Не удалось записать кэш списка вакансий: %s", exc)

    return response_model


@router.post("/{id}/refresh", response_model=VacancyRefreshResponse)
async def refresh_vacancy_expiry(
    id: int,
    db: AsyncSession = Depends(get_db),
) -> VacancyRefreshResponse:
    """Продлить срок действия вакансии на один календарный месяц."""
    stmt = (
        select(Vacancy)
        .where(Vacancy.id == id)
        .options(selectinload(Vacancy.candidates))
        .with_for_update()
    )
    result = await db.execute(stmt)
    vacancy = result.scalar_one_or_none()
    if vacancy is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Vacancy {id} not found",
        )

    old_expiry: datetime = vacancy.expiry_date
    vacancy.expiry_date = old_expiry + relativedelta(months=1)

    await db.commit()
    await db.refresh(vacancy)

    try:
        await delete_by_pattern(f"{VACANCY_CACHE_PREFIX}:*")
    except Exception as exc:  # noqa: BLE001
        logger.warning("Не удалось очистить кэш списка вакансий: %s", exc)

    return VacancyRefreshResponse(
        vacancy_id=vacancy.id,
        old_expiry_date=old_expiry,
        new_expiry_date=vacancy.expiry_date,
    )
