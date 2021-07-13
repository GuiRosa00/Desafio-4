from app import alunos
from app.association import association_alu_ativ
from app.extensions import db

class Atividade(db.Model):
    __tablename__ = 'atividade'
    #definicao das variaveis
    id = db.Column(db.Integer,primary_key = True)
    horario = db.Column(db.String(5),nullable = False)
    tipo = db.Column(db.String(15),nullable = False)
    lotacao = db.Column(db.Integer,nullable = False)
    professor_id = db.Column(db.Integer, db.ForeignKey('professor.id'))