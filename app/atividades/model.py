from app.association import association
from app.extensions import db

class Atividade(db.Model):
    __tablename__ ='atividade'
    #definicao das variaveis
    id = db.Column(db.Integer,primary_key = True)
    horario = db.Column(db.String(5),nullable = False)
    tipo = db.Column(db.String(15),nullable = False)
    lotacao = db.Column(db.Integer,nullable = False)
    alunos = db.relationship('Aluno',secondary = association, backref = db.backref('atividade'))
    def json(self):
        """json(self)-> dict
        Retorna as informações de uma atividade no formato json"""
        return {
            "id":self.id,
            "horario":self.horario,
            "tipo":self.tipo,
            "lotacao":self.lotacao,
            "alunos": [aluno.id for aluno in self.alunos],
        }