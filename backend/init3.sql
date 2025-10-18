CREATE TABLE IF NOT EXISTS account (
    id SERIAL PRIMARY KEY,
    login VARCHAR(254) NOT NULL,
    password_hash VARCHAR(60) NOT NULL,
    email VARCHAR(254) NOT NULL,
    created_at TIMESTAMPTZ,
    is_student BOOLEAN false,
    is_university BOOLEAN false,
    is_company BOOLEAN false,
    is_admin BOOLEAN false
);

-- Таблица кандидатов
CREATE TABLE IF NOT EXISTS candidate (
    id SERIAL PRIMARY KEY,
    account_id INTEGER REFERENCES account(id) ON DELETE CASCADE,
    surname VARCHAR(254) NOT NULL,
    name VARCHAR(254) NOT NULL,
    middle_name VARCHAR(254) NOT NULL,
    birth_date TIMESTAMPTZ NOT NULL
);

-- Таблицы-справочники регионов
CREATE TABLE IF NOT EXISTS region (
    id SERIAL PRIMARY KEY,
    title VARCHAR(254) NOT NULL UNIQUE
);

-- Таблицы-справочники городов
CREATE TABLE IF NOT EXISTS city (
    id SERIAL PRIMARY KEY,
    region_id INTEGER REFERENCES region(id) ON DELETE CASCADE,
    title VARCHAR(254) NOT NULL UNIQUE
);

-- Таблицы-справочники специализаций
/*
Возможно стоит не прописывать их статично (в случае компаний), а выявлять отталкиваясь от описанных проектов
Тогда у нас выстраивается логика: компания пишет описание проктов => оттуда выявляется список специализаций => 
=> на основе этого списка происходит поиск университетов
*/
CREATE TABLE IF NOT EXISTS specialization (
    id SERIAL PRIMARY KEY,
    title VARCHAR(254) NOT NULL,
    specialization_code VARCHAR(254) NOT NULL
);

-- Таблицы университетов
CREATE TABLE IF NOT EXISTS university (
    id SERIAL PRIMARY KEY,
    account_id INTEGER REFERENCES account(id) ON DELETE CASCADE,
    title VARCHAR(254) NOT NULL,
    city_id INTEGER REFERENCES city(id) ON DELETE CASCADE
);

-- Таблицы компаний
CREATE TABLE IF NOT EXISTS company (
    id SERIAL PRIMARY KEY,
    account_id INTEGER REFERENCES account(id) ON DELETE CASCADE,
    title VARCHAR(254) NOT NULL,
    city_id INTEGER NOT NULL REFERENCES city(id) ON DELETE CASCADE
);

/*
-- Таблица специализации для компаний
CREATE TABLE IF NOT EXISTS specialization_company (
    id SERIAL PRIMARY KEY,
    company_id INTEGER NOT NULL REFERENCES company(id) ON DELETE CASCADE,
    specialization_id INTEGER NOT NULL REFERENCES specialization(id) ON DELETE CASCADE
);
*/

-- Типы взаимодействий (не обязательно(!), но для записей, практик, работ, ЗАЯВКА)
CREATE TABLE IF NOT EXISTS interaction_type (
    id SERIAL PRIMARY KEY,
    code VARCHAR(254) NOT NULL UNIQUE,
    title VARCHAR(254) NOT NULL
);

-- Взаимодействия компаний и кандидатов
CREATE TABLE IF NOT EXISTS interaction (
    id SERIAL PRIMARY KEY,
    candidate_id INTEGER NOT NULL REFERENCES candidate(id) ON DELETE CASCADE,
    required_staff_id INTEGER NOT NULL REFERENCES required_staff(id) ON DELETE CASCADE,
    is_agreed BOOLEAN NOT NULL false,
    interaction_type INTEGER NOT NULL REFERENCES interaction_type(id) ON DELETE CASCADE,
    period_start TIMESTAMPTZ NOT NULL,
    period_end TIMESTAMPTZ,
    interaction_comment VARCHAR(1500)
);

-- Образование кандидатов
CREATE TABLE IF NOT EXISTS study (
    id SERIAL PRIMARY KEY,
    candidate_id INTEGER NOT NULL REFERENCES candidate(id) ON DELETE CASCADE,
    university_id INTEGER NOT NULL REFERENCES university(id) ON DELETE CASCADE,
    period_start TIMESTAMPTZ NOT NULL,
    period_end TIMESTAMPTZ,
    study_napr_id INTEGER NOT NULL REFERENCES study_napr(id) ON DELETE CASCADE
);

-- Образовательная программа / направление
CREATE TABLE IF NOT EXISTS educational_program (
    id SERIAL PRIMARY KEY,
    specialization_id INTEGER NOT NULL REFERENCES specialization(id) ON DELETE CASCADE,
    university_id INTEGER NOT NULL REFERENCES university(id) ON DELETE CASCADE
);

-- Дисциплина
CREATE TABLE IF NOT EXISTS subject (
    id SERIAL PRIMARY KEY,
    title VARCHAR(254) NOT NULL,
    description VARCHAR(1000),
    educational_program_id INTEGER NOT NULL REFERENCES educational_program(id) ON DELETE CASCADE
);

-- Рейтинг различных баллов по предметам
CREATE TABLE IF NOT EXISTS marks (
    id SERIAL PRIMARY KEY,
    subject_id INTEGER NOT NULL REFERENCES subject(id) ON DELETE CASCADE,
    candidate_id INTEGER NOT NULL REFERENCES candidate(id) ON DELETE CASCADE,
    mark INTEGER NOT NULL
);

-- Проект компании
CREATE TABLE IF NOT EXISTS project (
    id SERIAL PRIMARY KEY,
    title VARCHAR(254) NOT NULL,
    company_id INTEGER NOT NULL REFERENCES company(id) ON DELETE CASCADE,
    description VARCHAR(1000) NOT NULL
);

-- Требуемые кадры для проектов
CREATE TABLE IF NOT EXISTS required_staff (
    id SERIAL PRIMARY KEY,
    title VARCHAR(254) NOT NULL,
    description VARCHAR(1000) NOT NULL,
    is_approved BOOLEAN,
    project_id INTEGER NOT NULL REFERENCES project(id) ON DELETE CASCADE,
    specialization_id INTEGER NOT NULL REFERENCES specialization(id) ON DELETE CASCADE,
)

-- Требуемые навыки
CREATE TABLE IF NOT EXISTS subject_required_staff (
    id SERIAL PRIMARY KEY,
    subject_id INTEGER NOT NULL REFERENCES subject(id) ON DELETE CASCADE,
    required_staff_id INTEGER NOT NULL REFERENCES required_staff(id) ON DELETE CASCADE,
    additional_parameter INTEGER
)

-- Тип условия для вакансий
CREATE TABLE IF NOT EXISTS conditions_type (
    id SERIAL PRIMARY KEY,
    title VARCHAR(254) NOT NULL
)

-- Описанные условия вакансий
CREATE TABLE IF NOT EXISTS conditions_required_staff (
    id SERIAL PRIMARY KEY,
    required_staff_id INTEGER NOT NULL REFERENCES required_staff(id) ON DELETE CASCADE,
    condition_type_id INTEGER NOT NULL REFERENCES conditions_type(id) ON DELETE CASCADE,
    description VARCHAR(1000) NOT NULL
)

-- Подтверждение дополнительного образования вне университета
CREATE TABLE IF NOT EXISTS additional_education (
    id SERIAL PRIMARY KEY,
    subject_id INTEGER NOT NULL REFERENCES subject(id) ON DELETE CASCADE,
    candidate_id INTEGER NOT NULL REFERENCES candidate(id) ON DELETE CASCADE,
    certificate_link VARCHAR(500) NOT NULL,
)
