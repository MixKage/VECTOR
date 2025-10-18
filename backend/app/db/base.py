"""Декларативная база и импорт моделей для автогенерации Alembic."""

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Базовый класс декларативных моделей SQLAlchemy."""

    pass


def _import_models() -> None:
    """Импортировать модели для регистрации метаданных."""

    # pylint: disable=unused-import
    import app.models.candidate  # noqa: F401
    import app.models.intern  # noqa: F401
    import app.models.specialization  # noqa: F401
    import app.models.vacancy  # noqa: F401


_import_models()
