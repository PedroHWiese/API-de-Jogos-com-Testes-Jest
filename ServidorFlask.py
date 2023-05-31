
#Dependências que devem ser instaladas para que a API funcione
#pip install flask
#pip install mysql-connector-python

#importações do flask e mysql
from flask import Flask, jsonify, request 
import mysql.connector

#conexão com o banco de dados mysql
#O seu user e password devem corresponder com os que foram cadastrados no seu mysql, o nome da database 
#também deve ser alterados
mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='jogos',
)

#criação do servidor flask com o nome do arquivo atual nesse caso "app"
app = Flask(__name__)


#Rota para a criação de um novo jogo.
#O método (POST,DELETE,PUT...0) deve ser colocado no final da rota para indicar
#o "push" que será feito
@app.route('/jogos', methods=['POST'])
def incluir_novo_jogo(): #método

    #essa variável coleta o json com as informações colocadas e atribui elas a variável
    #json esse que pode ser visto usando o postman
    jogo = request.get_json()

    #esse código permite que o python execute comandos SQL 
    my_cursor = mydb.cursor()

    # as duas variáveis abaixo fazem um get do nome e plataforma do jogo que estão no json
    #para incluir eles no banco de dados

    nome_jogo = jogo.get('nome_jogo')
    plataforma_jogo = jogo.get('plataforma_jogo')

    #o comando sql que é necessário para colocar os valores novos no banco de dados
    #a sintaxe sql é mesma, apenas substituindo os values pela variáveis anteriores
    #que estão armazenando os dados passados pelo usuário
    sql = "INSERT INTO jogos (nome_jogo, plataforma_jogo) VALUES (%s, %s)"
    
    #esse if tem o intuito de checar se o nome do jogo ultrapassou o limite do banco de 45 caracteres
    #o código foi escrito dessa forma para fazer um teste analisando uma deficiência do banco desse tipo
    if len(nome_jogo) > 45:
        resposta = {'message': "O Nome do jogo é muito grande!"}
        status = 500  #500 = os dados não foram processados pelo banco

        #esse código return retorna a mensagem resposta passada acima e o status do servidor
        #que ocorreu, nesse caso 500 , a mesma sintaxe é usada no resto do código
        return resposta, status

    #esse verificação compara para ver se o jogo cadastrado não tem nome vazio
    #já que no banco foi colocar como not-null na área nome_jogo
    if nome_jogo != "" :

        #o comando sql é pego pelo cursor e executado, passando as duas variáveis como values
        #o db.commit é oque faz a ação final para o banco
        my_cursor.execute(sql, (nome_jogo, plataforma_jogo))
        mydb.commit()

        #resposta que retorna o jogo que acabou de ser cadastro como json e um mensagem abaixo que 
        #contem o nome do jogo, útil para fazer a veerificação do jest onde a mensagem deve incluir o nome dele
        resposta = {
            'jogo': jogo,
            'message': f"Jogo {nome_jogo} criado com sucesso"
        }
        #status 201 significa que o item foi cadastrado com sucesso
        status = 201 

        #o comando jsonify é oque de fato faz a resposta virar o json que pode ser visto
        return jsonify(resposta), status
    
    #se o jogo não passou no if anterior é por que ele não tem nome e o erro a seguir acontece
    else:
        
        resposta = {'message': "O Nome do jogo não pode ser nulo"}
        status = 422  #422 = os dados informados não fazem sentido ou não são reconhecidos pelo banco
        
        return resposta, status
        
    

# essa rota faz a consulta de todos os jogos no banco de dados a única diferença que fiz entre as rotas é o método 
#que atribui a cada uma, isso simplifica a API
@app.route('/jogos', methods=['GET'])
def obter_jogos(): #método

    #criação do cursor para segurar o banco e execução do comando que pega todos os itens do banco
    #novamente a sintaxe sql é a mesma que se fosse usar no banco de dados
    my_cursor = mydb.cursor()
    my_cursor.execute('SELECT * FROM jogos')

    #fetchall, como diz o nome ele vai pegar todos os itens e vai colocar em uma só variável 
    #que é a meus_jogos (pense no cursos como uma sacola)
    meus_jogos = my_cursor.fetchall()
    
    #crio uma lista para os jogos
    jogos = list()

    #pra cada jogo que se encontra no meu banco de dados, você vai imprimir sua ID, nome e plataforma
    for jogo in meus_jogos:
        jogos.append(
            {
                'id_jogo': jogo[0],
                'nome_jogo': jogo[1], 
                'plataforma_jogo':jogo[2]
            }
        )

    # resposta é um json de todos os jogos que estão no banco, eles vão ficar empilhados em ordem de ID
    resposta = ( jsonify(dados = jogos,))
    return resposta


#Essa rota faz a consulta de um jogo com id específico o método é GET porém na rota
#alteramos com um /<int:id> isso significa que o número que for escrito e pesquisado na hora
#o código vai salvar como variável e pesquisar no banco
@app.route('/jogos/<int:id>', methods=['GET'])
def obter_jogo_por_id(id):
    #mesmo código de cursor e comando, dessa vez usando o WHERE para filtar com onde a id_jogo == id da rota
    my_cursor = mydb.cursor()
    sql = "SELECT * FROM jogos WHERE id_jogo = %s"
    #comando sql é executado com id como parâmetro
    my_cursor.execute(sql, (id,))
    #ao invés de fecthall é fetchone, porque estão pegando apenas um dado 
    jogo = my_cursor.fetchone()

    #mesmo dicipnário de jogo usado na pesquisa passada, fazendo uma comparação if para ver sua existência
    #no banco de dados
    if jogo:
        jogo_dict = {
            'id_jogo': jogo[0],
            'nome_jogo': jogo[1],
            'plataforma_jogo': jogo[2]
        }
        resposta = jsonify(jogo=jogo_dict)
        return resposta
    
    #se o jogo não existir ele vai mandar a mensagem com status 404 "item não encontrado"
    else:
        resposta = jsonify(message='Jogo não encontrado')
        resposta.status_code = 404
        return resposta



#Essa rota usa o id passado na rota para encontrar no banco de dados e usa o método DELETE para remover ele do banco
#comparando com a ID existente 
@app.route('/jogos/<int:id>', methods=['DELETE'])
def excluir_jogo_por_id(id):

    #Mesmo esquema cursor-comando-executa com parâmetro-commita para o banco
    my_cursor = mydb.cursor()
    sql = "DELETE FROM jogos WHERE id_jogo = %s"
    my_cursor.execute(sql, (id,))
    mydb.commit()

    #comparação if para checar se o jogo existe no banco, se não existir ele volta com o mesmo erro de status 404
    if my_cursor.rowcount > 0:
        resposta = jsonify(message='Jogo excluído com sucesso')
        return resposta
    
    else:
        resposta = jsonify(message='Jogo não encontrado')
        resposta.status_code = 404
        return resposta



#Essa rota usa o método PUT para editar um jogo com uma id específica passada pelo usuário na rota
#igual como as duas rotas anteriores
@app.route('/jogos/<int:id>', methods=['PUT'])
def editar_jogo_por_id(id):

    #faz uma variável que guarda om request de json
    jogo_alterado = request.get_json()

    #nesse código temos que executar dois comandos sql um para encontrar o jogo e outro para inputar os
    #dados passados pelo usuário

    #cursor - comando - execução - fetch de um dado
    my_cursor = mydb.cursor()
    sql_select = "SELECT * FROM jogos WHERE id_jogo = %s"
    my_cursor.execute(sql_select, (id,))
    jogo = my_cursor.fetchone()

    #se o jogo que a id foi passada na rota existir ele segue no if
    #caso contrário ele retorna um erro de status 404
    if jogo:
        #pega os dois dados novos que foram passados no json e atribui a variáveis
        nome_jogo = jogo_alterado.get('nome_jogo', jogo[1])
        plataforma_jogo = jogo_alterado.get('plataforma_jogo', jogo[2])

        #usa as variáveis como atributos para esse novo comando sql para fazer a edição do item no banco de dados
        sql_update = "UPDATE jogos SET nome_jogo = %s, plataforma_jogo = %s WHERE id_jogo = %s"
        my_cursor.execute(sql_update, (nome_jogo, plataforma_jogo, id))
        mydb.commit()
        #json da resposta com a mensagem de sucesso
        resposta = jsonify(message='Jogo atualizado com sucesso')
       
        return resposta
    
    
    else:
        #mesmo erro e mesma mensagem como antes (eu atribui o erro de status direto a resposta aqui)
        resposta = jsonify(message='Jogo não encontrado')
        resposta.status_code = 404
        
        return resposta



#Run do servidor Flask
app.run(port=5000,host='localhost',debug=True)
