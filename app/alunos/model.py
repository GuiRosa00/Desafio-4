from app.extensions import db
from app import atividades

class Aluno(db.Model):
    __tablename__ = 'aluno'
    #definicao das variaveis
    id = db.Column(db.Integer,primary_key = True)
    nome = db.Column(db.String(30),nullable = False)
    genero = db.Column(db.String(10),nullable = False)
    endereco = db.Column(db.String(50),nullable = False)
    email = db.Column(db.String(100),unique = True,nullable = False)
    idade = db.Column(db.Integer,nullable = False)
    contato = db.Column(db.Integer,unique = True,nullable = False)
    cpf = db.Column(db.Integer,unique = True,nullable = False)
    senha_hash = db.Column(db.String(200),unique = True,nullable = False)
    def json(self):
        """json(self)-> dict
        Retorna as informações de um aluno no formato json"""
        return {
            "id":self.id, #está mantido para testes, na versão final será apagado
            "nome":self.nome,
            "genero":self.genero,
            "email":self.email,
            "idade":self.idade,
            "cpf":self.cpf,
            "atividades": [(atividade.horario,atividade.tipo) for atividade in self.atividade]
        }