"""Маршруты для работы с данными университетов."""

from __future__ import annotations

import logging
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.redis import get_recent, push_recent
from app.db.session import get_db
from app.models import Intern
from app.schemas import (
    UniversityCreate,
    UniversityRead,
    UniversityRecent,
    UniversityRecentResponse,
)

router = APIRouter()
logger = logging.getLogger(__name__)

UNIVERSITY_RECENT_KEY = "university:recent"


@router.post(
    "",
    response_model=UniversityRead,
    status_code=status.HTTP_201_CREATED,
)
async def register_university_interns(
    payload: UniversityCreate,
    db: AsyncSession = Depends(get_db),
) -> UniversityRead:
    """Сохранить данные о стажировках и добавить их в Redis."""
    intern = Intern(
        university_name=payload.university_name,
        direction_of_study_code=payload.direction_of_study_code,
        start_date=payload.start_date,
        end_time=payload.end_time,
        count=payload.count,
        reserved=0,
    )

    db.add(intern)
    await db.commit()
    await db.refresh(intern)

    recent_payload = {
        "university_name": intern.university_name,
        "direction_of_study_code": intern.direction_of_study_code,
        "start_date": intern.start_date,
        "end_time": intern.end_time,
        "count": intern.count,
        "submitted_at": datetime.now(timezone.utc),
    }

    try:
        await push_recent(UNIVERSITY_RECENT_KEY, recent_payload, max_length=100)
    except Exception as exc:  # noqa: BLE001
        logger.warning("Не удалось записать заявку университета в Redis: %s", exc)

    return intern


@router.get(
    "/latest",
    response_model=UniversityRecentResponse,
    status_code=status.HTTP_200_OK,
)
async def get_latest_university_submissions(limit: int = 10) -> UniversityRecentResponse:
    """Вернуть последние заявки университетов из Redis."""
    items = await get_recent(UNIVERSITY_RECENT_KEY, limit=limit)
    return UniversityRecentResponse(
        items=[UniversityRecent(**item) for item in items],
    )

