"""Агрегация маршрутов FastAPI."""

from fastapi import APIRouter

from app.api.routes import metrics, university, vacancies

api_router = APIRouter()
api_router.include_router(vacancies.router, prefix="/vacancies", tags=["vacancies"])
api_router.include_router(university.router, prefix="/university", tags=["university"])
api_router.include_router(metrics.router, prefix="/metrics", tags=["metrics"])

__all__ = ("api_router",)
