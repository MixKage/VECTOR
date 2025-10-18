"""Маршруты для приёма данных от университетов."""

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.models import Intern
from app.schemas import UniversityCreate, UniversityRead

router = APIRouter()


@router.post(
    "",
    response_model=UniversityRead,
    status_code=status.HTTP_201_CREATED,
)
async def register_university_interns(
    payload: UniversityCreate,
    db: AsyncSession = Depends(get_db),
) -> UniversityRead:
    """Сохранить информацию университета о доступных стажировочных местах."""
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
    return intern

