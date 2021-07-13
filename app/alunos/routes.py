from flask import Blueprint
from app.alunos.controller import AlunoGeral,AlunoID
aluno_api = Blueprint('aluno_api',__name__)
aluno_api.add_url_rule(
         '/aluno', view_func = AlunoGeral.as_view('aluno_create'), methods = ['GET','POST'])

aluno_api.add_url_rule(
         '/aluno/details/<int:id>',view_func = AlunoID.as_view('aluno_details'),methods = ['GET','PUT','PATCH','DELETE'])
