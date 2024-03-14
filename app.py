from flask import Flask, Response, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String
import _mysql_connector
import json

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:16042003@localhost/crud'

db = SQLAlchemy(app)
app.app_context().push()

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50))
    email = db.Column(db.String(100))

    def to_json(self):
        return {"id": self.id, "nome": self.nome, "email": self.email}

#selecionar todos
@app.route("/usuarios", methods=["GET"])
def seleciona_usuarios():
    usuarios_objetos = Usuario.query.all()
    usuarios_json = [usuario.to_json() for usuario in usuarios_objetos]
    return gera_response(200, "usuarios", usuarios_json, "ok")

#seleciona um
@app.route("/usuario/<id>", methods=["GET"])
def seleciona_usuario(id):
    usuario_obj = Usuario.query.filter_by(id =id).first()
    usuario_json = usuario_obj.to_json()
    return gera_response(200, "usuario", usuario_json, "usuario unico")


#cadastrar
@app.route("/usuario", methods=["POST"])
def cria_usuario():
    body = request.get_json()
    try:
        usuario = Usuario(nome=body["nome"], email=body["email"])
        db.session.add(usuario)
        db.session.commit()
        return gera_response(201, "usuario", usuario.to_json(), "usuario criado")
    except Exception as e:
        print(e)
        return gera_response(400, "usuario", {}, "error ao cadastrar")

#atualizar
@app.route("/usuario/<id>", methods=["PUT"])
def atualiza_usuario(id):
    usuario_obj = Usuario.query.filter_by(id =id).first()
    body = request.get_json()

    try:
        if('nome' in body):
            usuario_obj.nome = body["nome"]
        if("email" in body):
            usuario_obj.email = body["email"]

        db.session.add(usuario_obj)
        db.session.commit()
        return gera_response(200, "usuario", usuario_obj.to_json(), "usuario atualizado")
    except Exception as e:
        print("error", e)
        return gera_response(400, "usuario", {}, "error ao atualizar")

#delete
@app.route("/usuario/<id>", methods=["DELETE"])
def deletar_usuario(id):
    usuario_obj = Usuario.query.filter_by(id = id).first()

    try:
        db.session.delete(usuario_obj)
        db.session.commit()
        return gera_response(202, "usuario", usuario_obj.to_json(), "usuario deletado")
    except Exception as e:  
        print("error", e)
        return gera_response(400, "usuario", {}, "error ao deletar")

def gera_response(status, nome_do_conteudo, conteudo, mensagem=False):
    body = {}
    body[nome_do_conteudo] = conteudo

    if(mensagem):
        body["mensagem"] = mensagem

    return Response(json.dumps(body), status=status, mimetype="application/jason")

app.run(port=8085, host='0.0.0.0', debug=True, threaded=True)

