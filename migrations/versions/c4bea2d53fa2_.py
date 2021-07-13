"""empty message

Revision ID: c4bea2d53fa2
Revises: 
Create Date: 2021-07-13 16:31:12.508812

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c4bea2d53fa2'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('aluno',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nome', sa.String(length=30), nullable=False),
    sa.Column('genero', sa.String(length=10), nullable=False),
    sa.Column('endereco', sa.String(length=50), nullable=False),
    sa.Column('email', sa.String(length=100), nullable=False),
    sa.Column('idade', sa.Integer(), nullable=False),
    sa.Column('contato', sa.Integer(), nullable=False),
    sa.Column('cpf', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('contato'),
    sa.UniqueConstraint('cpf')
    )
    op.create_table('atividade',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('horario', sa.String(length=5), nullable=False),
    sa.Column('tipo', sa.String(length=15), nullable=False),
    sa.Column('lotacao', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('association',
    sa.Column('aluno', sa.Integer(), nullable=True),
    sa.Column('atividade', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['aluno'], ['aluno.id'], ),
    sa.ForeignKeyConstraint(['atividade'], ['atividade.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('association')
    op.drop_table('atividade')
    op.drop_table('aluno')
    # ### end Alembic commands ###