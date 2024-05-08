"""add tasks tables

Revision ID: d05b1687f24e
Revises: 177cf473c133
Create Date: 2024-05-08 20:51:08.464011

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "d05b1687f24e"
down_revision: Union[str, None] = "177cf473c133"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "task",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("description", sa.String(), nullable=False),
        sa.Column("author_id", sa.Integer(), nullable=True),
        sa.Column("charged_id", sa.Integer(), nullable=True),
        sa.Column("deadline", sa.DateTime(), nullable=False),
        sa.Column(
            "status",
            sa.Enum("wait", "process", "check", "success", name="statuses"),
            nullable=False,
        ),
        sa.Column("estimate", sa.Interval(), nullable=False),
        sa.ForeignKeyConstraint(
            ["author_id"], ["user.id"], ondelete="SET NULL"
        ),
        sa.ForeignKeyConstraint(
            ["charged_id"], ["user.id"], ondelete="SET NULL"
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("id"),
    )
    op.create_table(
        "task_executor",
        sa.Column("executor_id", sa.Integer(), nullable=False),
        sa.Column("task_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["executor_id"], ["user.id"], ondelete="CASCADE"
        ),
        sa.ForeignKeyConstraint(["task_id"], ["task.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("executor_id", "task_id"),
    )
    op.create_table(
        "task_observer",
        sa.Column("observer_id", sa.Integer(), nullable=False),
        sa.Column("task_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["observer_id"], ["user.id"], ondelete="CASCADE"
        ),
        sa.ForeignKeyConstraint(["task_id"], ["task.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("observer_id", "task_id"),
    )
    op.create_unique_constraint("unique_department_id", "department", ["id"])
    op.create_unique_constraint("unique_position_id", "position", ["id"])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint("unique_position_id", "position", type_="unique")
    op.drop_constraint("unique_department_id", "department", type_="unique")
    op.drop_table("task_observer")
    op.drop_table("task_executor")
    op.drop_table("task")
    # ### end Alembic commands ###
