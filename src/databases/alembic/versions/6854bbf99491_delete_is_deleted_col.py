"""delete is_deleted col

Revision ID: 6854bbf99491
Revises: 6c257b876b65
Create Date: 2023-12-16 09:21:30.712062

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6854bbf99491'
down_revision: Union[str, None] = '6c257b876b65'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
