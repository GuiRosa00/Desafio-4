from app.extensions import db

class Professor(db.Model):
    __tablename__ = 'professor'
    #definicao das variaveis
    id = db.Column(db.Integer,primary_key = True)
    nome = db.Column(db.String(30),nullable = False)
    genero = db.Column(db.String(10),nullable = False)
    endereco = db.Column(db.String(50),nullable = False)
    idade = db.Column(db.Integer,nullable = False)
    contato = db.Column(db.Integer,unique = True,nullable = False)
    cpf = db.Column(db.Integer,unique = True,nullable = False)
    atividades = db.relationship('Atividade',backref='professor')

    def json(self):
        return {
            "id":self.id,
            "nome":self.nome,
            "genero":self.genero,
            "idade":self.idade,
            "contato":self.contato,
            "cpf":self.cpf,
            "atividades": self.atividades
        }