"""init roles and core tables

Revision ID: 0001_init
Revises:
Create Date: 2025-10-18 00:00:00
"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "0001_init"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Create all base tables, constraints, indexes and seed roles."""

    # --- role ---
    op.create_table(
        "role",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("code", sa.Integer(), nullable=False, unique=True),
        sa.Column("title", sa.String(length=64), nullable=False, unique=True),
    )

    # --- account ---
    op.create_table(
        "account",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("login", sa.String(length=254), nullable=False, unique=True),
        sa.Column("password_hash", sa.String(length=100), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )

    # --- account_role (M2M) ---
    op.create_table(
        "account_role",
        sa.Column("account_id", sa.Integer(), sa.ForeignKey("account.id", ondelete="CASCADE"), primary_key=True),
        sa.Column("role_id", sa.Integer(), sa.ForeignKey("role.id", ondelete="CASCADE"), primary_key=True),
    )

    # --- region ---
    op.create_table(
        "region",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("title", sa.String(length=254), nullable=False, unique=True),
    )

    # --- city ---
    op.create_table(
        "city",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("region_id", sa.Integer(), sa.ForeignKey("region.id", ondelete="CASCADE")),
        sa.Column("title", sa.String(length=254), nullable=False),
        sa.UniqueConstraint("region_id", "title", name="uq_city_region_title"),
    )

    # --- specialization ---
    op.create_table(
        "specialization",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("title", sa.String(length=254), nullable=False),
        sa.Column("specialization_code", sa.String(length=254), nullable=False, unique=True),
    )

    # --- university ---
    op.create_table(
        "university",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("account_id", sa.Integer(), sa.ForeignKey("account.id", ondelete="CASCADE"), unique=True),
        sa.Column("title", sa.String(length=254), nullable=False),
        sa.Column("city_id", sa.Integer(), sa.ForeignKey("city.id", ondelete="CASCADE")),
    )

    # --- company ---
    op.create_table(
        "company",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("account_id", sa.Integer(), sa.ForeignKey("account.id", ondelete="CASCADE"), unique=True),
        sa.Column("title", sa.String(length=254), nullable=False),
        sa.Column("city_id", sa.Integer(), sa.ForeignKey("city.id", ondelete="CASCADE"), nullable=False),
    )

    # --- student ---
    op.create_table(
        "student",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("account_id", sa.Integer(), sa.ForeignKey("account.id", ondelete="CASCADE"), unique=True),
        sa.Column("surname", sa.String(length=254), nullable=False),
        sa.Column("name", sa.String(length=254), nullable=False),
        sa.Column("middle_name", sa.String(length=254), nullable=False),
        sa.Column("birth_date", sa.DateTime(timezone=True), nullable=False),
    )

    # --- specialization_company ---
    op.create_table(
        "specialization_company",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("company_id", sa.Integer(), sa.ForeignKey("company.id", ondelete="CASCADE"), nullable=False),
        sa.Column("specialization_id", sa.Integer(), sa.ForeignKey("specialization.id", ondelete="CASCADE"), nullable=False),
        sa.UniqueConstraint("company_id", "specialization_id", name="uq_specialization_company_pair"),
    )

    # --- interaction_type ---
    op.create_table(
        "interaction_type",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("code", sa.String(length=254), nullable=False, unique=True),
        sa.Column("title", sa.String(length=254), nullable=False),
    )

    # --- educational_program ---
    op.create_table(
        "educational_program",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("specialization_id", sa.Integer(), sa.ForeignKey("specialization.id", ondelete="CASCADE"), nullable=False),
        sa.Column("university_id", sa.Integer(), sa.ForeignKey("university.id", ondelete="CASCADE"), nullable=False),
        sa.UniqueConstraint("specialization_id", "university_id", name="uq_program_spec_uni"),
    )

    # --- study ---
    op.create_table(
        "study",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("student_id", sa.Integer(), sa.ForeignKey("student.id", ondelete="CASCADE"), nullable=False),
        sa.Column("university_id", sa.Integer(), sa.ForeignKey("university.id", ondelete="CASCADE"), nullable=False),
        sa.Column("period_start", sa.DateTime(timezone=True), nullable=False),
        sa.Column("period_end", sa.DateTime(timezone=True)),
        sa.Column("educational_program_id", sa.Integer(), sa.ForeignKey("educational_program.id", ondelete="CASCADE"), nullable=False),
        sa.CheckConstraint("period_end IS NULL OR period_end >= period_start", name="ck_study_period"),
    )

    # --- subject ---
    op.create_table(
        "subject",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("title", sa.String(length=254), nullable=False),
        sa.Column("description", sa.Text()),
        sa.Column("educational_program_id", sa.Integer(), sa.ForeignKey("educational_program.id", ondelete="CASCADE"), nullable=False),
    )

    # --- marks ---
    op.create_table(
        "marks",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("subject_id", sa.Integer(), sa.ForeignKey("subject.id", ondelete="CASCADE"), nullable=False),
        sa.Column("student_id", sa.Integer(), sa.ForeignKey("student.id", ondelete="CASCADE"), nullable=False),
        sa.Column("mark", sa.Integer(), nullable=False),
        sa.UniqueConstraint("subject_id", "student_id", name="uq_marks_subject_student"),
        sa.CheckConstraint("mark >= 0 AND mark <= 100", name="ck_marks_range"),
    )

    # --- project ---
    op.create_table(
        "project",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("title", sa.String(length=254), nullable=False),
        sa.Column("company_id", sa.Integer(), sa.ForeignKey("company.id", ondelete="CASCADE"), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
    )

    # --- required_staff ---
    op.create_table(
        "required_staff",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("title", sa.String(length=254), nullable=False),
        sa.Column("project_id", sa.Integer(), sa.ForeignKey("project.id", ondelete="CASCADE"), nullable=False),
        sa.Column("specialization_id", sa.Integer(), sa.ForeignKey("specialization.id", ondelete="CASCADE"), nullable=False),
    )

    # --- interaction ---
    op.create_table(
        "interaction",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("student_id", sa.Integer(), sa.ForeignKey("student.id", ondelete="CASCADE"), nullable=False),
        sa.Column("company_id", sa.Integer(), sa.ForeignKey("company.id", ondelete="CASCADE"), nullable=False),
        sa.Column("interaction_type_id", sa.Integer(), sa.ForeignKey("interaction_type.id", ondelete="CASCADE"), nullable=False),
        sa.Column("period_start", sa.DateTime(timezone=True), nullable=False),
        sa.Column("period_end", sa.DateTime(timezone=True)),
        sa.Column("interaction_comment", sa.String(length=254)),
        sa.CheckConstraint("period_end IS NULL OR period_end >= period_start", name="ck_interaction_period"),
    )

    # ----- Indexes on FKs (performance) -----
    op.create_index("idx_city_region_id", "city", ["region_id"])
    op.create_index("idx_university_city_id", "university", ["city_id"])
    op.create_index("idx_company_city_id", "company", ["city_id"])
    op.create_index("idx_student_account_id", "student", ["account_id"])
    op.create_index("idx_university_account_id", "university", ["account_id"])
    op.create_index("idx_company_account_id", "company", ["account_id"])
    op.create_index("idx_specialization_company_company_id", "specialization_company", ["company_id"])
    op.create_index("idx_specialization_company_spec_id", "specialization_company", ["specialization_id"])
    op.create_index("idx_interaction_student_id", "interaction", ["student_id"])
    op.create_index("idx_interaction_company_id", "interaction", ["company_id"])
    op.create_index("idx_interaction_type_id", "interaction", ["interaction_type_id"])
    op.create_index("idx_study_student_id", "study", ["student_id"])
    op.create_index("idx_study_university_id", "study", ["university_id"])
    op.create_index("idx_study_program_id", "study", ["educational_program_id"])
    op.create_index("idx_subject_program_id", "subject", ["educational_program_id"])
    op.create_index("idx_marks_subject_id", "marks", ["subject_id"])
    op.create_index("idx_marks_student_id", "marks", ["student_id"])
    op.create_index("idx_project_company_id", "project", ["company_id"])
    op.create_index("idx_required_staff_project_id", "required_staff", ["project_id"])
    op.create_index("idx_required_staff_spec_id", "required_staff", ["specialization_id"])

    # ----- Seed base roles -----
    role_table = sa.table(
        "role",
        sa.column("code", sa.Integer),
        sa.column("title", sa.String),
    )
    op.bulk_insert(
        role_table,
        [
            {"code": 0, "title": "no_role"},
            {"code": 1, "title": "admin"},
            {"code": 2, "title": "HR"},
            {"code": 3, "title": "university"},
            {"code": 4, "title": "student"},
        ],
    )


def downgrade() -> None:
    """Drop everything created in upgrade (reverse order to satisfy FKs)."""

    # indexes will be dropped automatically with tables; if needed, drop explicitly before tables.

    op.drop_table("interaction")
    op.drop_table("required_staff")
    op.drop_table("project")
    op.drop_table("marks")
    op.drop_table("subject")
    op.drop_table("study")
    op.drop_table("educational_program")
    op.drop_table("interaction_type")
    op.drop_table("specialization_company")
    op.drop_table("student")
    op.drop_table("company")
    op.drop_table("university")
    op.drop_table("specialization")
    op.drop_table("city")
    op.drop_table("region")
    op.drop_table("account_role")
    op.drop_table("account")
    op.drop_table("role")
