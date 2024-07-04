"""add disabled column to user

Revision ID: f494a9f1a212
Revises: 9c39ec29582e
Create Date: 2024-07-03 16:53:34.080404

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "f494a9f1a212"
down_revision: Union[str, None] = "9c39ec29582e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "users", sa.Column("disabled", sa.Boolean(), default=False, nullable=False)
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("users", "disabled")
    # ### end Alembic commands ###