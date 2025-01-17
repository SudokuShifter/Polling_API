"""revork and add model5

Revision ID: aab8df9f112d
Revises: 7987b05d7137
Create Date: 2024-11-19 17:59:51.300807

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'aab8df9f112d'
down_revision: Union[str, None] = '7987b05d7137'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('answers', sa.Column('point', sa.Boolean(), nullable=False))
    op.alter_column('answers', 'answer',
               existing_type=sa.BOOLEAN(),
               type_=sa.String(),
               existing_nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('answers', 'answer',
               existing_type=sa.String(),
               type_=sa.BOOLEAN(),
               existing_nullable=False)
    op.drop_column('answers', 'point')
    # ### end Alembic commands ###
