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

# Это объект конфигурации Alembic, дающий доступ к параметрам из .ini файла.
config = context.config

# Прочитать конфигурацию логирования из файла, если он указан.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Метаданные SQLAlchemy из Base приложения. Alembic использует их для
# автогенерации миграций на основе состояния моделей.
target_metadata = Base.metadata


def run_migrations_offline():
    """Запустить миграции в оффлайн-режиме.

    В оффлайн-режиме Alembic не подключается к базе данных и генерирует
    SQL-скрипты для выполнения вручную или записи в файл. Функция:
      1. Получает URL базы данных из конфигурации Alembic.
      2. Настраивает контекст миграций для генерации SQL (literal_binds).
      3. Запускает процесс миграций, который выводит SQL в stdout или в
         файл в зависимости от настроек Alembic.

    Эта функция не принимает аргументов и использует глобальный объект
    config для получения настроек.
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
    # Выполняем миграции в рамках транзакции (запись SQL).
    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection):
    """Выполнить миграции, используя синхронное соединение.

    Предназначена для вызова внутри AsyncEngine.run_sync: принимает
    синхронный объект Connection и настраивает Alembic для работы через
    это соединение. Функция:
      1. Конфигурирует Alembic с переданным соединением и метаданными.
      2. Запускает миграции в контексте транзакции.

    Args:
        connection: Синхронный объект sqlalchemy.engine.Connection,
            связанный с целевой базой данных.
    """
    # Настроить Alembic для использования переданного соединения.
    context.configure(connection=connection, target_metadata=target_metadata)
    # Выполнить миграции в рамках управляемой транзакции.
    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online():
    """Запустить миграции в онлайн-режиме с использованием AsyncEngine.

    Онлайн-режим подключается к базе данных и применяет миграции напрямую.
    Функция создаёт движок на основе URL из конфигурации Alembic, получает
    асинхронное соединение и выполняет синхронный helper do_run_migrations
    через connection.run_sync для корректной работы в асинхронном контексте.

    Порядок действий:
      1. Создать AsyncEngine, обёрнутый вокруг create_engine.
      2. Получить асинхронное соединение и вызвать run_sync(do_run_migrations).
      3. Освободить ресурсы движка после выполнения.

    Важно: движок создаётся с pool.NullPool, чтобы избежать переиспользования
    соединений при короткоживущих задачах миграции.
    """
    # Создаём AsyncEngine поверх синхронного create_engine для совместимости.
    connectable = AsyncEngine(
        create_engine(
            config.get_main_option("sqlalchemy.url"),
            poolclass=pool.NullPool,
            future=True,
        )
    )

    # Получаем асинхронное соединение и выполняем синхронный helper внутри run_sync.
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    # Закрываем и освобождаем ресурсы движка.
    await connectable.dispose()


# Выбрать режим выполнения миграций в зависимости от состояния контекста Alembic.
if context.is_offline_mode():
    run_migrations_offline()
else:
    import asyncio
    # Запустить асинхронный поток для онлайн-миграций.
    asyncio.run(run_migrations_online())
