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
            {
                "id": 3,
                "name": "Стажёр Frontend разработчик",
                "company": "WebVision",
                "field_file": "frontend_tasks.pdf",
                "platform": "HeadHunter",
                "specialization": "Frontend",
                "type_work": "Стажировка",
                "grafic": "Гибкий график",
                "place_work": "Екатеринбург",
                "map_link": "https://maps.example.com/webvision",
                "time": 20,
                "price": "38000 RUB",
                "additionally": "Опыт с React и менторство от старших разработчиков",
                "text": "Ищем стажёра для участия в разработке интерфейсов на React.",
                "site_link": "https://webvision.example.com/jobs/frontend-intern",
                "video_link": "https://video.example.com/frontend-intern",
                "personal_data": True,
                "emails_data": True,
                "sms": True,
                "creation_date": base_creation + timedelta(days=10),
                "expiry_date": base_creation + timedelta(days=40),
                "is_approved": True,
            },
            {
                "id": 4,
                "name": "Стажёр DevOps инженер",
                "company": "CloudSync",
                "field_file": "devops_intro.pdf",
                "platform": "HabrCareer",
                "specialization": "DevOps",
                "type_work": "Полная занятость",
                "grafic": "Офис / Удалённо",
                "place_work": "Новосибирск",
                "map_link": "https://maps.example.com/cloudsync",
                "time": 40,
                "price": "60000 RUB",
                "additionally": "Обучение CI/CD, работа с Docker и Kubernetes",
                "text": "Стажировка для DevOps-инженеров: настройка инфраструктуры, мониторинг и деплой.",
                "site_link": "https://cloudsync.example.com/careers/devops-intern",
                "video_link": None,
                "personal_data": True,
                "emails_data": False,
                "sms": False,
                "creation_date": base_creation + timedelta(days=15),
                "expiry_date": base_creation + timedelta(days=45),
                "is_approved": False,
            },
            {
                "id": 5,
                "name": "Стажёр UI/UX дизайнер",
                "company": "Designify",
                "field_file": "design_brief.pdf",
                "platform": "LinkedIn",
                "specialization": "UI/UX",
                "type_work": "Частичная занятость",
                "grafic": "Удалённо",
                "place_work": "Казань",
                "map_link": "https://maps.example.com/designify",
                "time": 30,
                "price": "42000 RUB",
                "additionally": "Портфолио-проект, ревью от арт-директора",
                "text": "Помощь в проектировании пользовательских интерфейсов и проведении UX-исследований.",
                "site_link": "https://designify.example.com/job/uiux-intern",
                "video_link": "https://video.example.com/uiux-intern",
                "personal_data": True,
                "emails_data": True,
                "sms": False,
                "creation_date": base_creation + timedelta(days=7),
                "expiry_date": base_creation + timedelta(days=37),
                "is_approved": True,
            },
            {
                "id": 6,
                "name": "Стажёр тестировщик",
                "company": "QualityLab",
                "field_file": "qa_checklist.docx",
                "platform": "HeadHunter",
                "specialization": "QA / Testing",
                "type_work": "Стажировка",
                "grafic": "Полный день",
                "place_work": "Ростов-на-Дону",
                "map_link": "https://maps.example.com/qualitylab",
                "time": 40,
                "price": "35000 RUB",
                "additionally": "Тренинг по тестированию, сертификат",
                "text": "Стажёр QA будет помогать в написании тест-кейсов и проверке web-приложений.",
                "site_link": "https://qualitylab.example.com/jobs/qa-intern",
                "video_link": None,
                "personal_data": True,
                "emails_data": True,
                "sms": True,
                "creation_date": base_creation + timedelta(days=12),
                "expiry_date": base_creation + timedelta(days=42),
                "is_approved": False,
            },
            {
                "id": 7,
                "name": "Стажёр ML инженер",
                "company": "NeuroSoft",
                "field_file": "ml_tasks.pdf",
                "platform": "LinkedIn",
                "specialization": "Machine Learning",
                "type_work": "Полная занятость",
                "grafic": "Гибкий график",
                "place_work": "Москва",
                "map_link": "https://maps.example.com/neurosoft",
                "time": 40,
                "price": "70000 RUB",
                "additionally": "GPU-серверы, участие в реальных проектах",
                "text": "Работа над моделями машинного обучения под руководством экспертов.",
                "site_link": "https://neurosoft.example.com/jobs/ml-intern",
                "video_link": "https://video.example.com/ml-intern",
                "personal_data": True,
                "emails_data": False,
                "sms": False,
                "creation_date": base_creation + timedelta(days=20),
                "expiry_date": base_creation + timedelta(days=50),
                "is_approved": True,
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
