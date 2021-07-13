from app.extensions import db

#associação das classes médico e paciente
association_med_pac = db.Table('association_med_pac',db.Model.metadata,
db.Column('medico', db.Integer, db.ForeignKey('medico.id')),
db.Column('paciente', db.Integer, db.ForeignKey('paciente.id')))