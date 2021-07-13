from flask import request,jsonify
from flask.views import MethodView
from app.atividades.model import Atividade
from app.extensions import db
from app.alunos.model import Aluno

class AtividadeGeral(MethodView): #/atividade
    def get(self):
        """get(self)->dict,int
        mostra as atividades cadastradas no sistema"""
        atividade = Atividade.query.all()
        return jsonify([atividade.json() for atividade in atividade]),200
    
    def post(self):
        """post(self)-> dict,int
        adiciona no sistema uma atividade"""
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
        """get(self,int)-> dict, int
        Dado um id, retorna uma atividade específica do sistema"""
        atividade = Atividade.query.get_or_404(id)
        return atividade.json(),200
    
    def put(self,id):
        """put(self,int)-> dict,int
        Dado um id, altera todas as informações de uma atividade do sistema e mostra as alterações"""
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
        """patch(self,int)-> dict, int
        Dado um id, verifica as informações do json e altera as necessárias no banco de dados de determinada atividade"""
        atividade = Atividade.query.get_or_404(id)
        dados = request.json
        horario = dados.get("horario",atividade.horario)
        tipo =dados.get("tipo",atividade.tipo)
        lotacao =dados.get("lotacao",atividade.lotacao)
        id_list = dados.get("alunos",atividade.alunos)

        #verificação dos dados
        listastr = [(horario,"horario"),(tipo,"tipo")]
        listaint = [(lotacao,"lotacao")]
        if id_list != []:
            for id_l in id_list:
                if not isinstance(id_l,int): return {"Error": f"Um ID não está tipado como Inteiro"}
        for dadoint,erro in listaint:
            if not isinstance(dadoint,int): return {"Error": f"O dado {erro} não está tipado como Inteiro"}
        for dadostr,erro in listastr:
            if (not isinstance(dadostr,str)) or dadostr == '': return {"Error": f"O dado {erro} não está tipado como String"}  
        
        for aluno in id_list:
            aluno = Aluno.query.get_or_404(aluno)
            if not(aluno in atividade.alunos):
                atividade.alunos.append(aluno)
        atividade.horario =horario
        atividade.tipo = tipo
        atividade.lotacao =lotacao
        db.session.commit()
        return atividade.json(),200
      
    def delete(self,id):
        """delete(self,int)-> dict, int
        Dado um ID, deleta a atividade possuinte do ID no banco de dados."""
        atividade  = Atividade.query.get_or_404(id)
        db.session.delete(atividade)
        db.session.commit()
        return atividade.json(), 200

class AtivaluRemove(MethodView): #atividade/details/id/aluno
    def delete(self,id):
        """delete(self,int)-> dict, int
        Dado um ID e um input json, deleta os alunos possuinte do ID no banco de dados da atividade."""
        atividade  = Atividade.query.get_or_404(id)
        dados = request.json
        id_list = dados.get("alunos",atividade.alunos)
        if id_list != []:
            for id_l in id_list:
                if not isinstance(id_l,int): return {"Error": f"Um ID não está tipado como Inteiro"}
        for aluno in id_list:
            aluno = Aluno.query.get_or_404(aluno)
            if aluno in atividade.alunos:
                atividade.alunos.remove(aluno)
        db.session.commit()
        return atividade.json(), 200

