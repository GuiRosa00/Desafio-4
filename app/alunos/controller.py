from flask import request,jsonify,render_template
from flask.views import MethodView
from app.alunos.model import Aluno
from app.extensions import db,mail
from flask_mail import Message

class AlunoGeral(MethodView): #/aluno
    def get(self):
        """get(self)->dict,int
        mostra todos os alunos cadastrados no sistema"""
        aluno = Aluno.query.all()
        return jsonify([aluno.json() for aluno in aluno]),200
    
    def post(self):
        """post(self)-> dict,int
        adiciona no sistema um aluno"""
        dados = request.json
        nome =dados.get("nome")
        genero = dados.get("genero")
        endereco =dados.get("endereco")
        email = dados.get("email")
        idade =dados.get("idade")
        contato = dados.get("contato")
        cpf = dados.get("cpf")
        
        #verificação dos dados
        listastr = [(nome,"nome"),(genero,"genero"),(endereco,"endereco"),(email,"email")]
        listaint = [(idade,"idade"),(contato, "contato"),(cpf,"cpf")]
        for dadoint,erro in listaint:
            if not isinstance(dadoint,int): return {"Error": f"O dado {erro} não está tipado como Inteiro"},406
        for dadostr,erro in listastr:
            if (not isinstance(dadostr,str)) or dadostr == '': return {"Error": f"O dado {erro} não está tipado como String"},406
        aluno = Aluno(nome = nome,genero=genero,endereco=endereco,email = email,idade=idade,contato=contato,cpf=cpf)
        db.session.add(aluno)
        db.session.commit()
        #msg = Message(sender = 'guilherme.rosa@poli.ufrj.br',recipients = [email],subject = 'Cadastro Feito',html= render_template(email.html, nome= nome))
        #mail.send(msg)
        return aluno.json(),200
    
class AlunoID(MethodView): #aluno/details/id
    def get(self,id):
        """get(self,int)-> dict, int
        Dado um id, retorna um aluno específico do sistema"""
        aluno = Aluno.query.get_or_404(id)
        return aluno.json(),200
    
    def put(self,id):
        """put(self,int)-> dict,int
        Dado um id, altera todas as informações de um aluno do sistema e mostra as alterações"""
        aluno = Aluno.query.get_or_404(id)
        dados = request.json
        nome =dados.get("nome")
        genero = dados.get("genero")
        endereco =dados.get("endereco")
        idade =dados.get("idade")
        contato = dados.get("contato")
        cpf = dados.get("cpf")
        email = dados.get("email")

        #verificação dos dados
        listastr = [(nome,"nome"),(genero,"genero"),(endereco,"endereco"),(email,"email")]
        listaint = [(idade,"idade"),(contato, "contato"),(cpf,"cpf")]
        for dadoint,erro in listaint:
            if not isinstance(dadoint,int): return {"Error": f"O dado {erro} não está tipado como Inteiro"},406
        for dadostr,erro in listastr:
            if not isinstance(dadostr,str): return {"Error": f"O dado {erro} não está tipado como String"},406
        aluno.nome =nome
        aluno.genero = genero
        aluno.endereco =endereco
        aluno.idade =idade
        aluno.contato = contato
        aluno.cpf = cpf
        aluno.email = email
        db.session.commit()
        return aluno.json(),200
       
    def patch(self,id):
        """patch(self,int)-> dict, int
        Dado um id, verifica as informações do json e altera as necessárias no banco de dados de determinado aluno"""
        aluno = Aluno.query.get_or_404(id)
        dados = request.json
        nome =dados.get("nome",aluno.nome)
        genero = dados.get("genero",aluno.genero)
        endereco =dados.get("endereco",aluno.endereco)
        idade =dados.get("idade",aluno.idade)
        contato = dados.get("contato",aluno.contato)
        cpf = dados.get("cpf",aluno.cpf)
        email = dados.get("email",aluno.email)

        #verificação dos dados
        listastr = [(nome,"nome"),(genero,"genero"),(endereco,"endereco"),(email,"email")]
        listaint = [(idade,"idade"),(contato, "contato"),(cpf,"cpf")]
        for dadoint,erro in listaint:
            if not isinstance(dadoint,int): return {"Error": f"O dado {erro} não está tipado como Inteiro"},406
        for dadostr,erro in listastr:
            if not isinstance(dadostr,str): return {"Error": f"O dado {erro} não está tipado como String"},406
        aluno.nome =nome
        aluno.genero = genero
        aluno.endereco =endereco
        aluno.idade =idade
        aluno.contato = contato
        aluno.cpf = cpf
        aluno.email = email
        db.session.commit()
        return aluno.json(),200
      
    def delete(self,id):
        """delete(self,int)-> dict, int
        Dado um ID, deleta o aluno possuinte do ID no banco de dados."""
        aluno= Aluno.query.get_or_404(id)
        db.session.delete(aluno)
        db.session.commit()
        return aluno.json(), 200
