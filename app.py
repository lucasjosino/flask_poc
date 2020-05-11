from flask import Flask, render_template, request, jsonify, Response
from flask_wtf.csrf import CSRFProtect
import sqlite3
import os
import json

app = Flask(__name__)
# SECRET_KEY = os.urandom(32)
# app.config['SECRET_KEY'] = SECRET_KEY
# csrf = CSRFProtect(app)
app.config['WTF_CSRF_CHECK_DEFAULT'] = False
app.config['JSON_AS_ASCII'] = False


# ---- FUNÇÕES ----


# converte uma lista de atributos em uma string
def limpaQuery(termo):
    termo = termo.replace("'","")
    termo = termo.replace('"','')
    termo = termo.replace(';','')
    termo = termo.replace('--','')
    return termo

# converte uma lista de atributos em uma string no formato de update
def convertQueryCreateTable(nomeCampoList,tipoList):
    query = ""
    dict = {
        'integer': 'INT',
        'string': 'VARCHAR',
        'decimal': 'FLOAT',
        'date': 'DATE'
    }
    # concatenação em string dos objetos vindos do usuário
    for x in range(len(tipoList)):
        query = query +nomeCampoList[x]+" "+dict[tipoList[x]]
        if x != len(tipoList)-1:
            query = query +", "
    # limpeza dos objetos inputados pelo usuário
    query = limpaQuery(query)
    return query

# converte uma lista de atributos em uma string no formato de columns
def convertQueryInsertIntoColumns(nomeCampoList):
    query = ""
    # concatenação em string dos objetos vindos do usuário
    for nome in nomeCampoList:
            # limpeza dos atributosinputados pelo usuário
        nome = limpaQuery(nome)
        if nome != "id":
            query = query +"'"+ nome +"'"+", "
    query = query[:-2]
    return query

# converte uma lista de atributos em uma string no formato de columns
def convertQueryInsertIntoValues(nomeCampoList):
    query = ""
    # concatenação em string dos objetos vindos do usuário
    for nome in nomeCampoList:
        # limpeza dos atributosinputados pelo usuário
        nome = limpaQuery(nome)
        if nome != "id":
            if  not type(nomeCampoList[nome]) is int or type(nomeCampoList[nome]) is float:
                nome = limpaQuery(nomeCampoList[nome])
            query = query +"'"+nome+"'"+", "
    query = query[:-2]
    return query

# converte uma lista de atributos em uma string no formato de columns
def convertQueryUpdate(nomeCampoList):
    query = ""
    # concatenação em string dos objetos vindos do usuário
    for nome in nomeCampoList:
        # limpeza dos atributosinputados pelo usuário
        column = limpaQuery(nome)
        if column != "id":
            if  not type(nomeCampoList[column]) is int or type(nomeCampoList[column]) is float:
                valor = limpaQuery(nomeCampoList[column])
            else:
                valor = nomeCampoList[column]
            query = query + column +"='"+str(valor)+"', "
    query = query[:-2]
    return query

# retorna as entidades ja cadastradas no banco
def getEntitiesDB():
    conn = sqlite3.connect('sqlite.db')
    c = conn.cursor()
    c.execute("SELECT name FROM sqlite_master WHERE type ='table' AND name NOT LIKE 'sqlite_%';")
    entities = []
    for row in c.fetchall():
        entities.append(row[0])
    return entities

# função genérica para get
def genericGet(entity):
    conn = sqlite3.connect('sqlite.db')
    c = conn.cursor()
    entity = limpaQuery(entity)
    c.execute("SELECT * FROM "+entity)
    results = c.fetchall();
    if results == []:
        return "não há objetos cadastrados nessa entidade"
    return results

# função genérica para getid
def genericGetID(entity,id):
    conn = sqlite3.connect('sqlite.db')
    c = conn.cursor()
    entity = limpaQuery(entity)
    c.execute("SELECT * FROM "+entity+" WHERE "+entity+".id = "+str(id))
    result = c.fetchone()
    if result == None:
        return "não há objeto cadastrado com esse ID"
    return result

# função genérica para post
def genericPost(objectJson,entity):
    conn = sqlite3.connect('sqlite.db')
    c = conn.cursor()
    entity = limpaQuery(entity)
    sql = "INSERT INTO "+entity+"("+convertQueryInsertIntoColumns(objectJson)+") VALUES ("+convertQueryInsertIntoValues(objectJson)+");"
    c.execute(sql)
    conn.commit()
    return "O objeto foi adicionado"

# função genérica para getid
def genericDelete(entity,id):
    conn = sqlite3.connect('sqlite.db')
    c = conn.cursor()
    entity = limpaQuery(entity)
    c.execute("DELETE FROM "+entity+" WHERE "+entity+".id = "+str(id))
    conn.commit()
    return "O objeto foi deletado"

# função genérica para getid
def genericUpdate(objectJson,entity,id):
    conn = sqlite3.connect('sqlite.db')
    c = conn.cursor()
    entity = limpaQuery(entity)
    try:
        sql = "UPDATE "+entity+" SET "+convertQueryUpdate(objectJson)+" WHERE "+entity+".id = "+str(id)
        c.execute(sql)
        conn.commit()
    except sqlite3.OperationalError: 
        return "não foi possível adicionar o objeto, O nome de algum dos atributos está errado!"
    return "O objeto foi atualizado"


# ---- TRATAMENTO DE ROTAS E ENDPOINTS ----


# rota para a página de gerenciamento
@app.route('/')
def home():
    conn = sqlite3.connect('sqlite.db')
    c = conn.cursor()
    c.execute("SELECT name FROM sqlite_master WHERE type ='table' AND name NOT LIKE 'sqlite_%';")
    entities = []
    # limpando os resultados por serem nome de tabela
    for row in c.fetchall():
        entities.append(row[0])
    return render_template('home.html')

# rota para retorno das entidades presentes no banco
@app.route('/entities')
def getEntities():
    entities = getEntitiesDB()
    return jsonify(entities)

# rota de get generica
@app.route('/<string:entity>', methods=['GET','POST'])
def get(entity):
    response = ""
    entities = getEntitiesDB()
    for x in range(len(entities)):
        entities[x] = entities[x].lower()
    if entity in entities:
        if request.method == 'GET':
                response = genericGet(entity)
        if request.method == 'POST':
            response = genericPost(request.get_json(),entity)
    return jsonify(response)

# rota de getid, delete e update generica
@app.route('/<string:entity>/<int:id>', methods=['GET','PUT','DELETE'])
def teste(entity,id):
    response = ""
    entities = getEntitiesDB()
    for x in range(len(entities)):
        entities[x] = entities[x].lower()
    if entity in entities:
        if request.method == 'GET':
            response = jsonify(genericGetID(entity,id))
        if request.method == 'DELETE':
            response = jsonify(genericDelete(entity,id))
        if request.method == 'PUT':
            response = jsonify(genericUpdate(request.get_json(),entity,id))
    return response

@app.route('/cadastramodelo', methods=['GET', 'POST'])
def cadastraModelo():
    conn = sqlite3.connect('sqlite.db')
    c = conn.cursor()
    nomemodelo = request.form.get('nomemodelo')
    nomeCampoList = request.form.getlist('nomecampo')
    tipoList = request.form.getlist('tipo')
    auxiliarquery = convertQueryCreateTable(nomeCampoList,tipoList)
    try:
        sql = 'create table "nome" (id INTEGER PRIMARY KEY AUTOINCREMENT, ?)'.replace("nome",nomemodelo)
        sql = sql.replace('?',auxiliarquery)
        c.execute(sql)
        return Response(status = 201)
    except:
        return Response(status = 500)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)