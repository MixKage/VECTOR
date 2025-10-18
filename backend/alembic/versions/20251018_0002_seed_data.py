"""Тестовые данные для основных таблиц."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "20251018_0002"
down_revision = "20251018_0001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    vacancy = sa.table(
        "vacancy",
        sa.column("id", sa.Integer),
        sa.column("name", sa.String),
        sa.column("company", sa.String),
        sa.column("field_file", sa.String),
        sa.column("platform", sa.String),
        sa.column("specialization", sa.String),
        sa.column("type_work", sa.String),
        sa.column("grafic", sa.String),
        sa.column("place_work", sa.String),
        sa.column("map_link", sa.String),
        sa.column("time", sa.Integer),
        sa.column("price", sa.String),
        sa.column("additionally", sa.String),
        sa.column("text", sa.String),
        sa.column("site_link", sa.String),
        sa.column("video_link", sa.String),
        sa.column("personal_data", sa.Boolean),
        sa.column("emails_data", sa.Boolean),
        sa.column("sms", sa.Boolean),
        sa.column("creation_date", sa.DateTime(timezone=True)),
        sa.column("expiry_date", sa.DateTime(timezone=True)),
        sa.column("is_approved", sa.Boolean),
    )

    base_creation = datetime(2025, 9, 1, 9, 0, tzinfo=timezone.utc)
    op.bulk_insert(
        vacancy,
        [
            {
                "id": 1,
                "name": "Стажёр Python разработчик",
                "company": "TechCorp",
                "field_file": "python_stack.pdf",
                "platform": "HeadHunter",
                "specialization": "Backend",
                "type_work": "Стажировка",
                "grafic": "Гибкий график",
                "place_work": "Москва",
                "map_link": "https://maps.example.com/techcorp",
                "time": 20,
                "price": "40000 RUB",
                "additionally": "Оплачиваемый обед, менторство",
                "text": "Ищем мотивированного стажёра в Python-команду.",
                "site_link": "https://techcorp.example.com/job/python-intern",
                "video_link": "https://video.example.com/python-intern",
                "personal_data": True,
                "emails_data": True,
                "sms": False,
                "creation_date": base_creation,
                "expiry_date": base_creation + timedelta(days=30),
                "is_approved": True,
            },
            {
                "id": 2,
                "name": "Стажёр Data Analyst",
                "company": "Insight Labs",
                "field_file": "analytics_roadmap.docx",
                "platform": "LinkedIn",
                "specialization": "Data Science",
                "type_work": "Частичная занятость",
                "grafic": "Удалённо",
                "place_work": "Санкт-Петербург",
                "map_link": "https://maps.example.com/insightlabs",
                "time": 25,
                "price": "45000 RUB",
                "additionally": "Доступ к обучающим курсам",
                "text": "Помощь в подготовке отчётов и анализе данных.",
                "site_link": "https://insightlabs.example.com/jobs/da-intern",
                "video_link": None,
                "personal_data": True,
                "emails_data": False,
                "sms": True,
                "creation_date": base_creation + timedelta(days=5),
                "expiry_date": base_creation + timedelta(days=40),
                "is_approved": False,
            },
        ],
    )

    candidate = sa.table(
        "candidate",
        sa.column("id", sa.Integer),
        sa.column("surname", sa.String),
        sa.column("name", sa.String),
        sa.column("middle_name", sa.String),
        sa.column("phone", sa.String),
        sa.column("email", sa.String),
        sa.column("cv_link", sa.String),
    )
    op.bulk_insert(
        candidate,
        [
            {
                "id": 1,
                "surname": "Иванов",
                "name": "Павел",
                "middle_name": "Алексеевич",
                "phone": "79001234567",
                "email": "pavel.ivanov@example.com",
                "cv_link": "https://cloud.example.com/cv/pavel-ivanov.pdf",
            },
            {
                "id": 2,
                "surname": "Петрова",
                "name": "Екатерина",
                "middle_name": "Игоревна",
                "phone": "79007654321",
                "email": "ekaterina.petrova@example.com",
                "cv_link": "https://cloud.example.com/cv/ekaterina-petrova.pdf",
            },
        ],
    )

    responsibilities_list = sa.table(
        "responsibilities_list",
        sa.column("id", sa.Integer),
        sa.column("vacancy_id", sa.Integer),
        sa.column("description", sa.String),
    )
    op.bulk_insert(
        responsibilities_list,
        [
            {
                "id": 1,
                "vacancy_id": 1,
                "description": "Разработка REST API на FastAPI под руководством ментора.",
            },
            {
                "id": 2,
                "vacancy_id": 1,
                "description": "Поддержка существующих сервисов и покрытие тестами.",
            },
            {
                "id": 3,
                "vacancy_id": 2,
                "description": "Сбор и очистка данных из внутренних систем.",
            },
            {
                "id": 4,
                "vacancy_id": 2,
                "description": "Подготовка визуализаций и презентаций для заказчиков.",
            },
        ],
    )

    conditions_list = sa.table(
        "conditions_list",
        sa.column("id", sa.Integer),
        sa.column("vacancy_id", sa.Integer),
        sa.column("description", sa.String),
    )
    op.bulk_insert(
        conditions_list,
        [
            {
                "id": 1,
                "vacancy_id": 1,
                "description": "Частичная занятость 20 часов в неделю.",
            },
            {
                "id": 2,
                "vacancy_id": 1,
                "description": "Оформление по договору стажировки, менторская программа.",
            },
            {
                "id": 3,
                "vacancy_id": 2,
                "description": "Работа полностью удалённо, гибкий график.",
            },
            {
                "id": 4,
                "vacancy_id": 2,
                "description": "Ежемесячные отчёты о прогрессе стажировки.",
            },
        ],
    )

    vacancy_candidate = sa.table(
        "vacancy_candidate",
        sa.column("id", sa.Integer),
        sa.column("vacancy_id", sa.Integer),
        sa.column("candidate_id", sa.Integer),
        sa.column("is_new", sa.Boolean),
        sa.column("is_approved", sa.Boolean),
    )
    op.bulk_insert(
        vacancy_candidate,
        [
            {
                "id": 1,
                "vacancy_id": 1,
                "candidate_id": 1,
                "is_new": True,
                "is_approved": False,
            },
            {
                "id": 2,
                "vacancy_id": 1,
                "candidate_id": 2,
                "is_new": False,
                "is_approved": True,
            },
            {
                "id": 3,
                "vacancy_id": 2,
                "candidate_id": 2,
                "is_new": True,
                "is_approved": False,
            },
        ],
    )

    specialization_maping = sa.table(
        "specialization_maping",
        sa.column("id", sa.Integer),
        sa.column("specialization", sa.String),
        sa.column("direction_of_study_code", sa.String),
    )
    op.bulk_insert(
        specialization_maping,
        [
            {
                "id": 1,
                "specialization": "Backend",
                "direction_of_study_code": "09.03.04",
            },
            {
                "id": 2,
                "specialization": "Data Science",
                "direction_of_study_code": "09.04.02",
            },
        ],
    )

    intern = sa.table(
        "intern",
        sa.column("id", sa.Integer),
        sa.column("university_name", sa.String),
        sa.column("direction_of_study_code", sa.String),
        sa.column("start_date", sa.DateTime(timezone=True)),
        sa.column("end_time", sa.DateTime(timezone=True)),
        sa.column("count", sa.Integer),
        sa.column("reserved", sa.Integer),
    )
    op.bulk_insert(
        intern,
        [
            {
                "id": 1,
                "university_name": "МФТИ",
                "direction_of_study_code": "09.03.04",
                "start_date": base_creation,
                "end_time": base_creation + timedelta(days=90),
                "count": 15,
                "reserved": 10,
            }
        ],
    )

    for seq_name, table_name in (
        ("vacancy_id_seq", "vacancy"),
        ("candidate_id_seq", "candidate"),
        ("responsibilities_list_id_seq", "responsibilities_list"),
        ("conditions_list_id_seq", "conditions_list"),
        ("vacancy_candidate_id_seq", "vacancy_candidate"),
        ("specialization_maping_id_seq", "specialization_maping"),
        ("intern_id_seq", "intern"),
    ):
        op.execute(
            sa.text(
                "SELECT setval(:seq_name, COALESCE((SELECT MAX(id) FROM "
                + table_name
                + "), 1))"
            ).bindparams(seq_name=seq_name)
        )


def downgrade() -> None:
    op.execute(sa.text("DELETE FROM vacancy_candidate WHERE id IN (1,2,3)"))
    op.execute(sa.text("DELETE FROM responsibilities_list WHERE id IN (1,2,3,4)"))
    op.execute(sa.text("DELETE FROM conditions_list WHERE id IN (1,2,3,4)"))
    op.execute(sa.text("DELETE FROM intern WHERE id = 1"))
    op.execute(sa.text("DELETE FROM specialization_maping WHERE id IN (1,2)"))
    op.execute(sa.text("DELETE FROM candidate WHERE id IN (1,2)"))
    op.execute(sa.text("DELETE FROM vacancy WHERE id IN (1,2)"))
