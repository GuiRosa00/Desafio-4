from flask import request,jsonify
from flask.views import MethodView
from app.professores.model import Professor
from app.extensions import db

class ProfessorGeral(MethodView): #/professor
    def get(self):
        professor = Professor.query.all()
        return jsonify([professor.json() for professor in professor]),200
    
    def post(self):
        dados = request.json
        nome =dados.get("nome")
        genero = dados.get("genero")
        endereco =dados.get("endereco")
        idade =dados.get("idade")
        contato = dados.get("contato")
        cpf = dados.get("cpf")
        #verificação dos dados
        listastr = [(nome,"nome"),(genero,"genero"),(endereco,"endereco")]
        listaint = [(idade,"idade"),(contato, "contato"),(cpf,"cpf")]
        for dadoint,erro in listaint:
            if not isinstance(dadoint,int): return {"Error": f"O dado {erro} não está tipado como Inteiro"}
        for dadostr,erro in listastr:
            if (not isinstance(dadostr,str)) or dadostr == '': return {"Error": f"O dado {erro} não está tipado como String"}  
        
        professor = Professor(nome = nome,genero=genero,endereco=endereco,idade=idade,contato=contato,cpf=cpf)
        db.session.add(professor)
        db.session.commit()
        return professor.json(),200
    
class ProfessorID(MethodView): #professor/details/id
    def get(self,id):
        professor = Professor.query.get_or_404(id)
        return professor.json(),200
    
    def put(self,id):
        professor = Professor.query.get_or_404(id)
        dados = request.json
        nome =dados.get("nome")
        genero = dados.get("genero")
        endereco =dados.get("endereco")
        idade =dados.get("idade")
        contato = dados.get("contato")
        cpf = dados.get("cpf")
        #verificação dos dados
        listastr = [(nome,"nome"),(genero,"genero"),(endereco,"endereco")]
        listaint = [(idade,"idade"),(contato, "contato"),(cpf,"cpf")]
        for dadoint,erro in listaint:
            if not isinstance(dadoint,int): return {"Error": f"O dado {erro} não está tipado como Inteiro"}
        for dadostr,erro in listastr:
            if (not isinstance(dadostr,str)) or dadostr == '': return {"Error": f"O dado {erro} não está tipado como String"}  
        
        professor.nome =nome
        professor.genero = genero
        professor.endereco =endereco
        professor.idade =idade
        professor.contato = contato
        professor.cpf = cpf
        db.session.commit()
        return professor.json(),200
       
    def patch(self,id):
        professor = Professor.query.get_or_404(id)
        dados = request.json
        nome =dados.get("nome",professor.nome)
        genero = dados.get("genero",professor.genero)
        endereco =dados.get("endereco",professor.endereco)
        idade =dados.get("idade",professor.idade)
        contato = dados.get("contato",professor.contato)
        cpf = dados.get("cpf",professor.cpf)

        #verificação dos dados
        listastr = [(nome,"nome"),(genero,"genero"),(endereco,"endereco")]
        listaint = [(idade,"idade"),(contato, "contato"),(cpf,"cpf")]
        for dadoint,erro in listaint:
            if not isinstance(dadoint,int): return {"Error": f"O dado {erro} não está tipado como Inteiro"}
        for dadostr,erro in listastr:
            if not isinstance(dadostr,str): return {"Error": f"O dado {erro} não está tipado como String"}  
        
        professor.nome =nome
        professor.genero = genero
        professor.endereco =endereco
        professor.idade =idade
        professor.contato = contato
        professor.cpf = cpf
        db.session.commit()
        return professor.json(),200
      
    def delete(self,id):
        professor  = Professor.query.get_or_404(id)
        db.session.delete(professor)
        db.session.commit()
        return professor.json(), 200