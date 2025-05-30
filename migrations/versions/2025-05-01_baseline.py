"""baseline

Revision ID: e2b3a048bb7a
Revises: 
Create Date: 2025-05-01 16:12:47.517895

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import advanced_alchemy


# revision identifiers, used by Alembic.
revision: str = 'e2b3a048bb7a'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('routes',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('hashed', sa.String(length=256), nullable=False),
    sa.Column('departure_at', sa.DateTime(), nullable=False),
    sa.Column('arrival_at', sa.DateTime(), nullable=False),
    sa.Column('created_at', advanced_alchemy.types.datetime.DateTimeUTC(timezone=True), nullable=False),
    sa.Column('updated_at', advanced_alchemy.types.datetime.DateTimeUTC(timezone=True), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_routes'))
    )
    op.create_index('idx_hashed_departure_at', 'routes', ['hashed', 'departure_at'], unique=False)
    op.create_table('stops',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=256), nullable=False),
    sa.Column('created_at', advanced_alchemy.types.datetime.DateTimeUTC(timezone=True), nullable=False),
    sa.Column('updated_at', advanced_alchemy.types.datetime.DateTimeUTC(timezone=True), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_stops'))
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('stops')
    op.drop_index('idx_hashed_departure_at', table_name='routes')
    op.drop_table('routes')
    # ### end Alembic commands ###
