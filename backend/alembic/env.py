from __future__ import annotations
from logging.config import fileConfig
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from alembic import context
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncEngine

import os, sys
sys.path.append(os.path.abspath("."))

from app.db.session import Base
from app.db import models  # noqa: F401

# Это объект конфигурации Alembic, дающий доступ к значениям из .ini файла.
config = context.config

# Прочитать конфигурацию логирования из файла, если он указан.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Метаданные SQLAlchemy из Base приложения. Alembic использует их для
# автогенерации миграций на основе состояния моделей.
target_metadata = Base.metadata


def run_migrations_offline():
    """Запустить миграции в режиме 'offline'.

    В оффлайн-режиме Alembic генерирует SQL-скрипты без подключения к БД.
    Эта функция настраивает контекст миграций с URL из конфигурации
    Alembic и затем выполняет миграции (вывод SQL).
    """
    # Получаем URL базы данных из .ini-конфигурации Alembic.
    url = config.get_main_option("sqlalchemy.url")
    # Настраиваем контекст миграций для генерации SQL без подключения.
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    # Начинаем транзакцию и запускаем миграции (запись SQL в выходной поток
    # или файл в зависимости от настроек Alembic).
    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection):
    """Выполнить миграции, используя предоставленное синхронное соединение.

    Предназначена для вызова внутри AsyncEngine.run_sync — функция принимает
    синхронный объект Connection и настраивает Alembic на использование
    этого соединения для применения миграций.

    Args:
        connection: Объект Connection SQLAlchemy, подключённый к целевой БД.
    """
    # Настроить Alembic для использования данного соединения и метаданных
    # проекта (нужно для автогенерации и применения миграций).
    context.configure(connection=connection, target_metadata=target_metadata)
    # Выполнить миграции в рамках транзакции, управляемой Alembic.
    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online():
    """Запустить миграции в 'online' режиме с использованием AsyncEngine.

    Онлайн-режим подключается к базе и применяет миграции напрямую.
    Функция создаёт AsyncEngine из URL в конфигурации Alembic, получает
    асинхронное соединение и делегирует выполнение синхронному помощнику
    do_run_migrations через run_sync.

    По завершении движок освобождает ресурсы.
    """
    # Создаём движок (synchronous engine), обёрнутый в AsyncEngine для совместимости.
    connectable = AsyncEngine(
        create_engine(
            config.get_main_option("sqlalchemy.url"),
            poolclass=pool.NullPool,
            future=True,
        )
    )

    # Получаем асинхронное соединение и запускаем синхронный helper
    # внутри run_sync, чтобы корректно выполнить миграции.
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    # Освобождаем ресурсы движка (соединения, пулы).
    await connectable.dispose()


# Выбираем режим выполнения миграций в зависимости от режима Alembic.
# При онлайн-режиме используем asyncio для запуска асинхронной функции.
if context.is_offline_mode():
    run_migrations_offline()
else:
    import asyncio

    asyncio.run(run_migrations_online())
