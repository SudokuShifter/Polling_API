"""revork2

Revision ID: 0479f726d893
Revises: 029646cb4bdd
Create Date: 2024-11-16 21:50:11.383327

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0479f726d893'
down_revision: Union[str, None] = '029646cb4bdd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user_results', sa.Column('result', sa.Integer(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user_results', 'result')
    # ### end Alembic commands ###
