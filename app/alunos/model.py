from app.extensions import db
from app.association import association_alu_ativ

class Aluno(db.Model):
    __tablename__ = 'aluno'
    #definicao das variaveis
    id = db.Column(db.Integer,primary_key = True)
    nome = db.Column(db.String(30),nullable = False)
    genero = db.Column(db.String(10),nullable = False)
    endereco = db.Column(db.String(50),nullable = False)
    idade = db.Column(db.Integer,nullable = False)
    contato = db.Column(db.Integer,unique = True,nullable = False)
    cpf = db.Column(db.Integer,unique = True,nullable = False)
    atividades = db.relationship('Atividade',secondary = association_alu_ativ, backref = db.backref('aluno'))