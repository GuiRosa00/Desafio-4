from flask import request,jsonify,render_template
from flask_mail import Message
from flask.views import MethodView
from flask_jwt_extended import create_access_token,jwt_required,get_jwt_identity
import bcrypt

from app.alunos.model import Aluno
from app.extensions import db,mail
from app.atividades.model import Atividade
from app import templates


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
        senha = dados.get("senha")
        
        #verificação dos dados
        listastr = [(nome,"nome"),(genero,"genero"),(endereco,"endereco"),(email,"email"),(senha,"senha")]
        listaint = [(idade,"idade"),(contato, "contato"),(cpf,"cpf")]
        for dadoint,erro in listaint:
            if not isinstance(dadoint,int): return {"Error": f"O dado {erro} não está tipado como Inteiro"},406
        for dadostr,erro in listastr:
            if (not isinstance(dadostr,str)) or dadostr == '': return {"Error": f"O dado {erro} não está tipado como String"},406
        
        #verificação dos dados unique
        lista_unique = [(Aluno.query.filter_by(email = email).first(),"Email"),(Aluno.query.filter_by(cpf = cpf).first(),"CPF"),(Aluno.query.filter_by(contato = contato).first(),"Contato")]
        for dado_unique, erro in lista_unique:
            if dado_unique: return {"Error": f"Já tem o mesmo {erro} cadastrado no sistema"},400
        if not "@" in email : return {"Error": "Não foi inserido um email válido"},400
        if idade<0: return {"Error": 'Foi inserido uma Idade inferior a 0'},400

        senha_hash = bcrypt.hashpw(senha.encode(),bcrypt.gensalt())
        aluno = Aluno(nome = nome,genero=genero,endereco=endereco,email = email,idade=idade,contato=contato,cpf=cpf,senha_hash= senha_hash)
        db.session.add(aluno)
        db.session.commit()
        
        msg = Message(sender = 'guilherme.rosa@poli.ufrj.br',
        recipients = [email],subject = 'Cadastro Feito',
        html= render_template('email.html', nome= nome))
        mail.send(msg)
        return aluno.json(),200
    
class AlunoID(MethodView): #aluno/details/id
    decorators = [jwt_required()]
    def get(self,id):
        """get(self,int)-> dict, int
        Dado um id, retorna um aluno específico do sistema"""
        #verificação do token
        auth_id = get_jwt_identity()
        if id != auth_id: return {"Erro":"O usuário é diferente do token criado"},400
        
        aluno = Aluno.query.get_or_404(id)
        return aluno.json(),200
    
    def put(self,id):
        """put(self,int)-> dict,int
        Dado um id, altera todas as informações de um aluno do sistema e mostra as alterações"""
        #verificação do token
        auth_id = get_jwt_identity()
        if id != auth_id: return {"Erro":"O usuário é diferente do token criado"},400

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
        if not "@" in email : return {"Error": "Não foi inserido um email válido"},400
        if idade<0: return {"Error": 'Foi inserido uma Idade inferior a 0'},400
        
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
        #verificação do token
        auth_id = get_jwt_identity()
        if id != auth_id: return {"Erro":"O usuário é diferente do token criado"},400
        
        aluno = Aluno.query.get_or_404(id)
        dados = request.json
        nome =dados.get("nome",aluno.nome)
        genero = dados.get("genero",aluno.genero)
        endereco =dados.get("endereco",aluno.endereco)
        idade =dados.get("idade",aluno.idade)
        contato = dados.get("contato",aluno.contato)
        cpf = dados.get("cpf",aluno.cpf)
        email = dados.get("email",aluno.email)
        id_list = dados.get("atividades",[])
        senha = dados.get("senha",'')
        #verificação dos dados
        listastr = [(nome,"nome"),(genero,"genero"),(endereco,"endereco"),(email,"email"),(senha,"senha")]
        listaint = [(idade,"idade"),(contato, "contato"),(cpf,"cpf")]
        if id_list != []:
            for id_l in id_list:
                if not isinstance(id_l,int): return {"Error": f"Um ID não está tipado como Inteiro"},406
        for dadoint,erro in listaint:
            if not isinstance(dadoint,int): return {"Error": f"O dado {erro} não está tipado como Inteiro"},406
        for dadostr,erro in listastr:
            if not isinstance(dadostr,str): return {"Error": f"O dado {erro} não está tipado como String"},406
        if not "@" in email : return {"Error": "Não foi inserido um email válido"},400
        if idade<0: return {"Error": 'Foi inserido uma Idade inferior a 0'},400
        #alteração dos dados normais
        aluno.nome =nome
        aluno.genero = genero
        aluno.endereco =endereco
        aluno.idade =idade
        aluno.contato = contato
        aluno.cpf = cpf
        aluno.email = email
        #alteração da senha
        if senha != '':
            senha = bcrypt.hashpw(senha.encode(),bcrypt.gensalt())
            aluno.senha_hash = senha
        #verificação das atividades
        for atividade in id_list:
            atividade = Atividade.query.get_or_404(atividade)
            if not(aluno in atividade.alunos) and (len(atividade.alunos)+1 <= atividade.lotacao):
                atividade.alunos.append(aluno)
            else: return {"Error": f"A atividade de {atividade.tipo} feita as {atividade.horario} está lotada."}
        db.session.commit()
        return aluno.json(),200
      
    def delete(self,id):
        """delete(self,int)-> dict, int
        Dado um ID, deleta o aluno possuinte do ID no banco de dados."""
        #verificação do token
        auth_id = get_jwt_identity()
        if id != auth_id: return {"Erro":"O usuário é diferente do token criado"},400
        
        aluno= Aluno.query.get_or_404(id)
        db.session.delete(aluno)
        db.session.commit()
        return aluno.json(), 200

class AlunoRemove(MethodView):#aluno/id/remove_atividade
    decorators = [jwt_required()]
    def delete(self,id):
        """delete(self,int)-> dict, int
        Dado um ID e um input json, deleta o aluno de todas as atividades dentro do input json."""
        #verificação do token
        auth_id = get_jwt_identity()
        if id != auth_id: return {"Erro":"O usuário é diferente do token criado"},400
        
        aluno  = Aluno.query.get_or_404(id)
        dados = request.json
        id_list = dados.get("atividades",[])
        
        #verificao dos dados
        if id_list == []: return {"Error": "A lista de ID está vazia"},406
        
        for id_l in id_list:
            if not isinstance(id_l,int): return {"Error": "Um ID não está tipado como Inteiro"},406
        
        #remocao do aluno das atividades
        for atividade in id_list:
            atividade = Atividade.query.get_or_404(atividade)
            if aluno in atividade.alunos:
                atividade.alunos.remove(aluno)
        db.session.commit()
        return aluno.json(), 200

class AlunoLogin(MethodView):#aluno/login
    def post(self):
        dados = request.json
        email = dados.get('email')
        senha = dados.get('senha')
        if not isinstance(email,str): return {"Erro": "Dado do email não está tipado como String"},400
        if not isinstance(senha,str): return {"Erro": "Dado da senha não está tipado como String"},400
        
        aluno = Aluno.query.filter_by(email=email).first()
        if not aluno or not bcrypt.checkpw(senha.encode(),aluno.senha_hash): 
            return {"Erro":"Email ou Senha Inválidos"},403
        token = create_access_token(identity=aluno.id)
        return {"token":token},200

