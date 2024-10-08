"""put list of objects respectively for all models

Revision ID: 646622361d39
Revises: 4c23a7c8adf4
Create Date: 2024-09-16 23:11:37.373112

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '646622361d39'
down_revision: Union[str, None] = '4c23a7c8adf4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('category', 'sub_categories')
    op.drop_column('product', 'options')
    op.drop_column('sub_category', 'products')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('sub_category', sa.Column('products', postgresql.JSON(astext_type=sa.Text()), autoincrement=False, nullable=True))
    op.add_column('product', sa.Column('options', postgresql.JSON(astext_type=sa.Text()), autoincrement=False, nullable=True))
    op.add_column('category', sa.Column('sub_categories', postgresql.JSON(astext_type=sa.Text()), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
