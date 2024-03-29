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
        professor = dados.get("professor")
        sala = dados.get("sala")
        dia = dados.get("dia")
        
        #verificação dos dados
        listastr = [(horario,"horario"),(tipo,"tipo"),(professor,"professor"),(sala,"sala"),(dia,"dia")]
        listaint = [(lotacao,"lotacao")]
        for dadoint,erro in listaint:
            if not isinstance(dadoint,int): return {"Error": f"O dado {erro} não está tipado como Inteiro"},406
        for dadostr,erro in listastr:
            if (not isinstance(dadostr,str)) or dadostr == '': return {"Error": f"O dado {erro} não está tipado como String"},406 
        database = Atividade.query.filter_by(sala = sala)
        for ativ in database:
            if horario == ativ.horario and dia == ativ.dia: return {"Error": "Já existe uma atividade nesta sala no mesmo horário e dia"},400
        if lotacao>5 or lotacao<0: return {"Error": "A lotação pedida excede o limite de 5 alunos ou é um número negativo"},400
        
        atividade = Atividade(horario = horario,tipo=tipo,lotacao=lotacao,professor = professor, sala = sala,dia = dia)
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
        professor = dados.get("professor")
        sala = dados.get("sala")
        dia = dados.get("dia")
        
        #verificação dos dados
        listastr = [(horario,"horario"),(tipo,"tipo"),(professor,"professor"),(sala,"sala"),(dia,"dia")]
        listaint = [(lotacao,"lotacao")]
        for dadoint,erro in listaint:
            if not isinstance(dadoint,int): return {"Error": f"O dado {erro} não está tipado como Inteiro"},406
        for dadostr,erro in listastr:
            if (not isinstance(dadostr,str)) or dadostr == '': return {"Error": f"O dado {erro} não está tipado como String"},406 
        if lotacao>5 or lotacao<0: return {"Error": "A lotação pedida excede o limite de 5 alunos ou é um número negativo"},400

        atividade.horario =horario
        atividade.tipo = tipo
        atividade.lotacao =lotacao
        atividade.professor = professor
        atividade.sala = sala
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
        id_list = dados.get("alunos",[])
        professor = dados.get("professor",atividade.professor)
        sala = dados.get("sala",atividade.sala)
        dia = dados.get("dia", atividade.dia)

        #verificação dos dados
        listastr = [(horario,"horario"),(tipo,"tipo"),(professor,"professor"),(sala,"sala"),(dia,"dia")]
        listaint = [(lotacao,"lotacao")]

        if id_list != []:
            for id_l in id_list:
                if not isinstance(id_l,int): return {"Error": f"Um ID não está tipado como Inteiro"},406
        for dadoint,erro in listaint:
            if not isinstance(dadoint,int): return {"Error": f"O dado {erro} não está tipado como Inteiro"},406
        for dadostr,erro in listastr:
            if (not isinstance(dadostr,str)) or dadostr == '': return {"Error": f"O dado {erro} não está tipado como String ou está no formato ''"},406  
        
        #verificações referente à lotação
        if lotacao>5 or lotacao<0: return {"Error": "A lotação pedida excede o limite de 5 alunos ou é um número negativo"},400
        if lotacao < len(atividade.alunos): return {"Error": "A lotação da atividade ficaria menor que o número de alunos inseridos."},403
        if len(id_list)>atividade.lotacao-len(atividade.alunos):return {"Error": "O número de alunos inscritos na atividade excederia sua lotação"},403
        
        #Adicao dos dados
        for aluno in id_list:
            aluno = Aluno.query.get_or_404(aluno)
            if not(aluno in atividade.alunos):
                atividade.alunos.append(aluno)
        atividade.horario =horario
        atividade.tipo = tipo
        atividade.lotacao =lotacao
        atividade.professor = professor
        atividade.sala = sala
        atividade.dia = dia
        db.session.commit()
        return atividade.json(),200
      
    def delete(self,id):
        """delete(self,int)-> dict, int
        Dado um ID, deleta a atividade possuinte do ID no banco de dados."""
        atividade  = Atividade.query.get_or_404(id)
        db.session.delete(atividade)
        db.session.commit()
        return atividade.json(), 200

class AtivaluRemove(MethodView): #atividade/id/remove/aluno
    def delete(self,id):
        """delete(self,int)-> dict, int
        Dado um ID e um input json, deleta os alunos possuinte do ID JSON no banco de dados da atividade."""
        atividade  = Atividade.query.get_or_404(id)
        dados = request.json
        id_list = dados.get("alunos",[])
        
        #verificao dos dados
        if id_list == []: return {"Error": "A lista de ID está vazia"},406
        
        for id_l in id_list:
            if not isinstance(id_l,int): return {"Error": "Um ID não está tipado como Inteiro"},406
        
        #remocao dos alunos
        for aluno in id_list:
            aluno = Aluno.query.get_or_404(aluno)
            if aluno in atividade.alunos:
                atividade.alunos.remove(aluno)
        db.session.commit()
        return atividade.json(), 200

