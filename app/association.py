from app.extensions import db

#associação das classes médico e paciente
association_alu_ativ = db.Table('association_alu_ativ',db.Model.metadata,
db.Column('aluno', db.Integer, db.ForeignKey('aluno.id')),
db.Column('atividade', db.Integer, db.ForeignKey('atividade.id')))