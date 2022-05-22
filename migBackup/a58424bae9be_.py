"""empty message

Revision ID: a58424bae9be
Revises: 467a40844818
Create Date: 2022-04-15 07:32:40.847102

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a58424bae9be'
down_revision = '467a40844818'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('question', sa.Column('picture_path', sa.String(length=500), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('question', 'picture_path')
    # ### end Alembic commands ###