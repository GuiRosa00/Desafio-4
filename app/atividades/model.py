from app.association import association
from app.extensions import db

class Atividade(db.Model):
    __tablename__ ='atividade'
    #definicao das variaveis
    id = db.Column(db.Integer,primary_key = True)
    horario = db.Column(db.String(5),nullable = False)
    tipo = db.Column(db.String(15),nullable = False)
    lotacao = db.Column(db.Integer,nullable = False)
    professor = db.Column(db.String(50),nullable = False)
    sala = db.Column(db.String(20),nullable = False)
    dia = db.Column(db.String(7),nullable = False)
    alunos = db.relationship('Aluno',secondary = association, backref = db.backref('atividade'))
    def json(self):
        """json(self)-> dict
        Retorna as informações de uma atividade no formato json"""
        return {
            "id":self.id,
            "horario":self.horario,
            "tipo":self.tipo,
            "lotacao":self.lotacao,
            "professor": self.professor,
            "sala": self.sala,
            "dia": self.dia,
            "alunos": [aluno.nome for aluno in self.alunos]
        }