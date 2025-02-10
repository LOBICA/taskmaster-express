"""add fields to users for fb login

Revision ID: bf0cb680436c
Revises: 7784b898ebe9
Create Date: 2024-06-13 16:04:54.412586

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "bf0cb680436c"
down_revision: Union[str, None] = "7784b898ebe9"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("users", sa.Column("name", sa.String(), nullable=False))
    op.add_column("users", sa.Column("fb_user_id", sa.String(), nullable=True))
    op.add_column("users", sa.Column("fb_access_token", sa.String(), nullable=True))
    op.alter_column("users", "password", existing_type=sa.VARCHAR(), nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column("users", "password", existing_type=sa.VARCHAR(), nullable=False)
    op.drop_column("users", "fb_access_token")
    op.drop_column("users", "fb_user_id")
    op.drop_column("users", "name")
    # ### end Alembic commands ###
