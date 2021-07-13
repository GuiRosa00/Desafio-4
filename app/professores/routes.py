from flask import Blueprint
from app.professores.controller import ProfessorGeral,ProfessorID
professor_api = Blueprint('professor_api',__name__)
professor_api.add_url_rule(
         '/professor', view_func = ProfessorGeral.as_view('professor_create'), methods = ['GET','POST'])

professor_api.add_url_rule(
         '/professor/details/<int:id>',view_func = ProfessorID.as_view('professor_details'),methods = ['GET','PUT','PATCH','DELETE'])
