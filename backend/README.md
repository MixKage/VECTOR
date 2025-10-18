# BACKEND версия 0.0.1

## Состав проекта

- **FastAPI** + **Nginx** для балансировки
- **PostgreSQL** и **Redis** как инфраструктурные сервисы
- **React (Vite)** клиент для frontend

## Предварительные требования

- Docker Desktop / Docker Engine + Docker Compose

## Запуск через Docker Compose

```bash
cp .env.example .env
docker-compose up --build
```

Приложение доступно на http://127.0.0.1:8080 (весь трафик проходит через Nginx). 

## Карта сервисов

- **Nginx** — точка входа http://127.0.0.1:8080
  - SPA (React) обслуживается по корню /
  - API проброшен по префиксу /api (например, http://127.0.0.1:8080/api/auth)
  - Swagger UI: http://127.0.0.1:8080/docs
  - OpenAPI JSON: http://127.0.0.1:8080/openapi.json
- **PostgreSQL**: порт 5432
- **Redis**: порт 6379

## Работа с миграциями

Миграции Alembic можно прогонять внутри контейнера API:

```bash
docker-compose exec api1 alembic upgrade head
```

## Структура ролей (коды → подписи)

| Код | Название        |
|-----|-----------------|
| 0   | Без роли        |
| 1   | Администратор   |
| 2   | HR              |
| 3   | Университет     |
| 4   | Студент         |
