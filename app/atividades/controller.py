from flask import request,jsonify
from flask.views import MethodView
from app.atividades.model import Atividade
from app.extensions import db
from app.alunos.model import Aluno

class AtividadeGeral(MethodView): #/atividade
    def get(self):
        atividade = Atividade.query.all()
        return jsonify([atividade.json() for atividade in atividade]),200
    
    def post(self):
        dados = request.json
        horario = dados.get("horario")
        tipo =dados.get("tipo")
        lotacao =dados.get("lotacao")
        #verificação dos dados
        listastr = [(horario,"horario"),(tipo,"tipo")]
        listaint = [(lotacao,"lotacao")]
        for dadoint,erro in listaint:
            if not isinstance(dadoint,int): return {"Error": f"O dado {erro} não está tipado como Inteiro"}
        for dadostr,erro in listastr:
            if (not isinstance(dadostr,str)) or dadostr == '': return {"Error": f"O dado {erro} não está tipado como String"}  
        
        atividade = Atividade(horario = horario,tipo=tipo,lotacao=lotacao)
        db.session.add(atividade)
        db.session.commit()
        return atividade.json(),200
    
class AtividadeID(MethodView): #atividade/details/id
    def get(self,id):
        atividade = Atividade.query.get_or_404(id)
        return atividade.json(),200
    
    def put(self,id):
        atividade = Atividade.query.get_or_404(id)
        dados = request.json
        horario = dados.get("horario")
        tipo =dados.get("tipo")
        lotacao =dados.get("lotacao")

        #verificação dos dados
        listastr = [(horario,"horario"),(tipo,"tipo")]
        listaint = [(lotacao,"lotacao")]
        for dadoint,erro in listaint:
            if not isinstance(dadoint,int): return {"Error": f"O dado {erro} não está tipado como Inteiro"}
        for dadostr,erro in listastr:
            if (not isinstance(dadostr,str)) or dadostr == '': return {"Error": f"O dado {erro} não está tipado como String"}  
        atividade.horario =horario
        atividade.tipo = tipo
        atividade.lotacao =lotacao
        db.session.commit()
        return atividade.json(),200
       
    def patch(self,id):
        atividade = Atividade.query.get_or_404(id)
        dados = request.json
        horario = dados.get("horario",atividade.horario)
        tipo =dados.get("tipo",atividade.tipo)
        lotacao =dados.get("lotacao",atividade.lotacao)

        #verificação dos dados
        listastr = [(horario,"horario"),(tipo,"tipo")]
        listaint = [(lotacao,"lotacao")]
        for dadoint,erro in listaint:
            if not isinstance(dadoint,int): return {"Error": f"O dado {erro} não está tipado como Inteiro"}
        for dadostr,erro in listastr:
            if (not isinstance(dadostr,str)) or dadostr == '': return {"Error": f"O dado {erro} não está tipado como String"}  
        atividade.horario =horario
        atividade.tipo = tipo
        atividade.lotacao =lotacao
        db.session.commit()
        return atividade.json(),200
      
    def delete(self,id):
        atividade  = Atividade.query.get_or_404(id)
        db.session.delete(atividade)
        db.session.commit()
        return atividade.json(), 200
