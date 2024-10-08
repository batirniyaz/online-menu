"""add created and updated at field to category

Revision ID: 2db213272c6c
Revises: 6372ed51ab90
Create Date: 2024-09-16 14:19:47.000286

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2db213272c6c'
down_revision: Union[str, None] = '6372ed51ab90'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('category', sa.Column('sort_order', sa.Integer(), nullable=False))
    op.add_column('category', sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False))
    op.add_column('category', sa.Column('updated_at', sa.TIMESTAMP(timezone=True), nullable=False))
    op.create_index(op.f('ix_category_sort_order'), 'category', ['sort_order'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_category_sort_order'), table_name='category')
    op.drop_column('category', 'updated_at')
    op.drop_column('category', 'created_at')
    op.drop_column('category', 'sort_order')
    # ### end Alembic commands ###
