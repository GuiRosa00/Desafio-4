from flask import Flask
from app.config import Config
from app.extensions import db,migrate
from app.alunos.routes import aluno_api
from app.atividades.routes import atividade_api
from app.professores.routes import professor_api

def create_app():
    """create_app(None)-> object
    Cria o app do Flask utilizado como back-end do sistema"""
    app = Flask(__name__)
    app.config.from_object(Config)
    
    #metodos registrados pelo Blueprint
    app.register_blueprint(aluno_api)
    app.register_blueprint(atividade_api)
    app.register_blueprint(professor_api)

    db.init_app(app)
    migrate.init_app(app,db)
    return app
