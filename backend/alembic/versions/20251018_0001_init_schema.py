"""Начальная схема, сформированная"""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "20251018_0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "vacancy",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(length=254), nullable=False),
        sa.Column("company", sa.String(length=254), nullable=False),
        sa.Column("field_file", sa.String(length=254), nullable=False),
        sa.Column("platform", sa.String(length=254), nullable=False),
        sa.Column("specialization", sa.String(length=254), nullable=False),
        sa.Column("type_work", sa.String(length=254), nullable=True),
        sa.Column("grafic", sa.String(length=254), nullable=True),
        sa.Column("place_work", sa.String(length=254), nullable=True),
        sa.Column("map_link", sa.String(length=254), nullable=True),
        sa.Column("time", sa.Integer(), nullable=True),
        sa.Column("price", sa.String(length=50), nullable=True),
        sa.Column("additionally", sa.String(length=500), nullable=True),
        sa.Column("text", sa.String(length=500), nullable=True),
        sa.Column("site_link", sa.String(length=50), nullable=True),
        sa.Column("video_link", sa.String(length=50), nullable=True),
        sa.Column("personal_data", sa.Boolean(), nullable=True),
        sa.Column("emails_data", sa.Boolean(), nullable=True),
        sa.Column("sms", sa.Boolean(), nullable=True),
        sa.Column("creation_date", sa.DateTime(timezone=True), nullable=False),
        sa.Column("expiry_date", sa.DateTime(timezone=True), nullable=False),
        sa.Column(
            "is_approved",
            sa.Boolean(),
            nullable=False,
            server_default=sa.text("false"),
        ),
    )

    op.create_table(
        "candidate",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("surname", sa.String(length=254), nullable=False),
        sa.Column("name", sa.String(length=254), nullable=False),
        sa.Column("middle_name", sa.String(length=254), nullable=False),
        sa.Column("phone", sa.String(length=11), nullable=False),
        sa.Column("email", sa.String(length=50), nullable=False),
        sa.Column("cv_link", sa.String(length=254), nullable=False),
    )

    op.create_table(
        "intern",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("university_name", sa.String(length=254), nullable=False),
        sa.Column("direction_of_study_code", sa.String(length=30), nullable=False),
        sa.Column("start_date", sa.DateTime(timezone=True), nullable=False),
        sa.Column("end_time", sa.DateTime(timezone=True), nullable=False),
        sa.Column("count", sa.Integer(), nullable=False),
        sa.Column("reserved", sa.Integer(), nullable=False),
    )

    op.create_table(
        "specialization_maping",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("specialization", sa.String(length=254), nullable=False),
        sa.Column("direction_of_study_code", sa.String(length=30), nullable=False),
    )

    op.create_table(
        "conditions_list",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("vacancy_id", sa.Integer(), nullable=False),
        sa.Column("description", sa.String(length=500), nullable=False),
        sa.ForeignKeyConstraint(
            ["vacancy_id"], ["vacancy.id"], ondelete="CASCADE"
        ),
    )

    op.create_table(
        "responsibilities_list",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("vacancy_id", sa.Integer(), nullable=False),
        sa.Column("description", sa.String(length=500), nullable=False),
        sa.ForeignKeyConstraint(
            ["vacancy_id"], ["vacancy.id"], ondelete="CASCADE"
        ),
    )

    op.create_table(
        "vacancy_candidate",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("vacancy_id", sa.Integer(), nullable=False),
        sa.Column("candidate_id", sa.Integer(), nullable=False),
        sa.Column(
            "is_new",
            sa.Boolean(),
            nullable=False,
            server_default=sa.text("true"),
        ),
        sa.Column(
            "is_approved",
            sa.Boolean(),
            nullable=False,
            server_default=sa.text("false"),
        ),
        sa.ForeignKeyConstraint(
            ["candidate_id"], ["candidate.id"], ondelete="CASCADE"
        ),
        sa.ForeignKeyConstraint(
            ["vacancy_id"], ["vacancy.id"], ondelete="CASCADE"
        ),
    )


def downgrade() -> None:
    op.drop_table("vacancy_candidate")
    op.drop_table("responsibilities_list")
    op.drop_table("conditions_list")
    op.drop_table("specialization_maping")
    op.drop_table("intern")
    op.drop_table("candidate")
    op.drop_table("vacancy")
