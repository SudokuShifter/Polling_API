"""revork and add model6

Revision ID: b0a10205f95a
Revises: aab8df9f112d
Create Date: 2024-11-20 14:58:59.287760

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b0a10205f95a'
down_revision: Union[str, None] = 'aab8df9f112d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('answers_poll_id_fkey', 'answers', type_='foreignkey')
    op.drop_column('answers', 'poll_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('answers', sa.Column('poll_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.create_foreign_key('answers_poll_id_fkey', 'answers', 'polls', ['poll_id'], ['id'])
    # ### end Alembic commands ###
