"""add phone number to user

Revision ID: 9c39ec29582e
Revises: 4563004932e5
Create Date: 2024-07-02 15:48:58.806044

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "9c39ec29582e"
down_revision: Union[str, None] = "4563004932e5"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("users", sa.Column("phone_number", sa.String(), nullable=True))
    op.create_unique_constraint(None, "users", ["phone_number"])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "users", type_="unique")
    op.drop_column("users", "phone_number")
    # ### end Alembic commands ###
