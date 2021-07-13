from app.extensions import db
from app.alunos.model import Aluno

#associação das classes alunos e atividades
association = db.Table('association',db.Model.metadata,
db.Column('aluno', db.Integer, db.ForeignKey('aluno.id')),
db.Column('atividade', db.Integer, db.ForeignKey('atividade.id')))