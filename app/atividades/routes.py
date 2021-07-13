from flask import Blueprint
from app.atividades.controller import AtividadeGeral,AtividadeID
atividade_api = Blueprint('atividade_api',__name__)
atividade_api.add_url_rule(
         '/atividade', view_func = AtividadeGeral.as_view('atividade_create'), methods = ['GET','POST'])

atividade_api.add_url_rule(
         '/atividade/details/<int:id>',view_func = AtividadeID.as_view('atividade_details'),methods = ['GET','PUT','PATCH','DELETE'])

atividade_api.add_url_rule(
         '/atividade/details/<int:id>/aluno',view_func = AtividadeID.as_view('atividade_aluno'),methods = ['PATCH'])
