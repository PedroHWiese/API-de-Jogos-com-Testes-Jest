
#pip install flask
#pip install mysql-connector-python

from flask import Flask, jsonify, request 
import mysql.connector

#conexão com o banco de dados mysql
mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='jogos',
)

#criação do servidor flask com o nome do arquivo atual nesse caso "app"
app = Flask(__name__)


# Criar um novo jogo
@app.route('/jogos', methods=['POST'])
def incluir_novo_jogo():
    jogo = request.get_json()

    my_cursor = mydb.cursor()

    nome_jogo = jogo.get('nome_jogo')
    plataforma_jogo = jogo.get('plataforma_jogo')

    sql = "INSERT INTO jogos (nome_jogo, plataforma_jogo) VALUES (%s, %s)"
    
    if len(nome_jogo) > 45:
        resposta = {'message': "O Nome do jogo é muito grande!"}
        status = 500  #500 = os dados não foram processados pelo banco
        return resposta, status

    if nome_jogo != "" :

        my_cursor.execute(sql, (nome_jogo, plataforma_jogo))
        mydb.commit()

        resposta = {
            'jogo': jogo,
            'message': f"Jogo {nome_jogo} criado com sucesso"
        }
        status = 201 #201 = jogo

        return jsonify(resposta), status
    else:
        
        resposta = {'message': "O Nome do jogo não pode ser nulo"}
        status = 422  #422 = os dados informados não fazem sentido ou não são reconhecidos
        
        
        return resposta, status


    

# Consultar todos os jogos do banco de dados 
@app.route('/jogos', methods=['GET'])
def obter_jogos():

    my_cursor = mydb.cursor()
    my_cursor.execute('SELECT * FROM jogos')
    meus_jogos = my_cursor.fetchall()
    
    jogos = list()

    for jogo in meus_jogos:
        jogos.append(
            {
                'id_jogo': jogo[0],
                'nome_jogo': jogo[1], 
                'plataforma_jogo':jogo[2]
            }
        )

    resposta = ( jsonify(dados = jogos,))
    return resposta


# Consultar um jogo específico do banco de dados
@app.route('/jogos/<int:id>', methods=['GET'])
def obter_jogo_por_id(id):
    my_cursor = mydb.cursor()
    sql = "SELECT * FROM jogos WHERE id_jogo = %s"
    my_cursor.execute(sql, (id,))
    jogo = my_cursor.fetchone()

    if jogo:
        jogo_dict = {
            'id_jogo': jogo[0],
            'nome_jogo': jogo[1],
            'plataforma_jogo': jogo[2]
        }
        resposta = jsonify(jogo=jogo_dict)
        return resposta
    else:
        resposta = jsonify(message='Jogo não encontrado')
        resposta.status_code = 404
        return resposta

#Deleta um jogo com o ID específicado e remove ele do banco de dados
@app.route('/jogos/<int:id>', methods=['DELETE'])
def excluir_jogo_por_id(id):
    my_cursor = mydb.cursor()
    sql = "DELETE FROM jogos WHERE id_jogo = %s"
    my_cursor.execute(sql, (id,))
    mydb.commit()

    if my_cursor.rowcount > 0:
        resposta = jsonify(message='Jogo excluído com sucesso')
        return resposta
    
    else:
        resposta = jsonify(message='Jogo não encontrado')
        resposta.status_code = 404
        return resposta


#Edita um jogo com ID específica
@app.route('/jogos/<int:id>', methods=['PUT'])
def editar_jogo_por_id(id):
    jogo_alterado = request.get_json()

    my_cursor = mydb.cursor()
    sql_select = "SELECT * FROM jogos WHERE id_jogo = %s"
    my_cursor.execute(sql_select, (id,))
    jogo = my_cursor.fetchone()

    if jogo:
        nome_jogo = jogo_alterado.get('nome_jogo', jogo[1])
        plataforma_jogo = jogo_alterado.get('plataforma_jogo', jogo[2])


        sql_update = "UPDATE jogos SET nome_jogo = %s, plataforma_jogo = %s WHERE id_jogo = %s"
        my_cursor.execute(sql_update, (nome_jogo, plataforma_jogo, id))
        mydb.commit()

        resposta = jsonify(message='Jogo atualizado com sucesso')
       
        return resposta
    
    
    else:
        resposta = jsonify(message='Jogo não encontrado')
        resposta.status_code = 404
        
        return resposta



#Run do servidor Flask
app.run(port=5000,host='localhost',debug=True)
