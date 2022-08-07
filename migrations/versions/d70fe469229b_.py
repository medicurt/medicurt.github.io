"""empty message

Revision ID: d70fe469229b
Revises: 42c3496d1a58
Create Date: 2022-07-31 12:01:14.000352

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'd70fe469229b'
down_revision = '42c3496d1a58'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('permissions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('permissions', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
    sa.Column('updated_by', sa.Integer(), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    sa.ForeignKeyConstraint(['updated_by'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_permissions_id'), 'permissions', ['id'], unique=False)
    op.add_column('user', sa.Column('permissions_id', sa.Integer(), nullable=False))
    op.create_index(op.f('ix_user_permissions_id'), 'user', ['permissions_id'], unique=False)
    op.create_foreign_key(None, 'user', 'permissions', ['permissions_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'user', type_='foreignkey')
    op.drop_index(op.f('ix_user_permissions_id'), table_name='user')
    op.drop_column('user', 'permissions_id')
    op.drop_index(op.f('ix_permissions_id'), table_name='permissions')
    op.drop_table('permissions')
    # ### end Alembic commands ###
