//instalar o nodeJS

//npm install axios
//npm install jest
const axios = require('axios');


//----------------------------------------------------------------------------------------------------------
/*
Aqui nesse arquivo estão escritos dos 10 testes do jest (linguagem javascripts) que vão rodar
usando as rotas da API como base e passando atributos e testando as respostas que vamos obter
por isso retornar os status de sucesso e erro assim como uma mensagem escrita são importantes
*/
//----------------------------------------------------------------------------------------------------------

//nome do teste que vai ser feito
test('POST -> Método "Cria um jogo com o nome Quake" ', async ()=>{
     
    //Preparar o cenário
    let jogo = 
    {
        "nome_jogo": "Quake", 
        "plataforma_jogo": "PS1"
    }

    //o que ocorre aqui é a reponse sendo um teste de post na rota abaixo usando os parâmetros
    //passados acima no método (o parâmetro é passado com a sintaxe do json)
    const response =
    await axios.post('http://localhost:5000/jogos', jogo);

    //a reposta esperada por esse teste deve ser um status 201 com uma mensagem dentro do json
    expect(response.status).toBe(201);
    expect(response.data).toHaveProperty('message','Jogo Quake criado com sucesso');

});

//----------------------------------------------------------------------------------------------------------


test('POST -> Método "Cria um jogo com nome de caracteres além do limite" ', async ()=>{

    let jogo = 
    {
        "nome_jogo": "XD".repeat(46),
        "plataforma_jogo": "PS2"
    }

    //essa parte do código faz um teste de erro
    //usando o axious, isso é para fazer um catch do erro de status que o teste vai passar
    await axios.post('http://localhost:5000/jogos', jogo).catch(
        function(error){
            if (error.response){
                expect(error.response.status).toBe(500);
                expect(error.response.data).toEqual({ message: 'O Nome do jogo é muito grande!' });

            }
        });

});

//----------------------------------------------------------------------------------------------------------


test('POST ->Método "Criar um jogo sem nome', async () =>{
    let jogo = {
        nome_jogo: "",
        plataforma_jogo:"PS2"
    }

    await axios.post('http://localhost:5000/jogos', jogo).catch(
        function(error){
            if (error.response){
                expect(error.response.status).toBe(422);

            }
        });

});


//----------------------------------------------------------------------------------------------------------

test('GET->Método "Todos os jogos do banco estão sendo listados ?', async()=>{
    const response = await axios('http://localhost:5000/jogos');
    expect(response.status).toBe(200);

});


//----------------------------------------------------------------------------------------------------------
test('GET->Método "Lista um jogo com Id específico" ', async()=>{
    const id_jogo = 4;
    const response = await axios.get(`http://localhost:5000/jogos/${id_jogo}`);
    expect(response.data.jogo).toHaveProperty('id_jogo',id_jogo);

});

//----------------------------------------------------------------------------------------------------------
test('GET->Método "Tenta listar um jogo que não existe" ', async()=>{
    const id_jogo = 1000;
    await axios.get(`http://localhost:5000/jogos/${id_jogo}`).catch(
        function(error){
            if (error.response){
                expect(error.response.status).toBe(404);

            }
        });

});


//----------------------------------------------------------------------------------------------------------
test('DELETE-> Método deve deletar e retornar a mensagem de exclusão do jogo', async () => {
    const id_jogo = 4;
    const response = await axios.delete(`http://localhost:5000/jogos/${id_jogo}`);
    
    expect(response.status).toBe(200);
    expect(response.data).toEqual({ message: 'Jogo excluído com sucesso' });
  });


//----------------------------------------------------------------------------------------------------------
test('DELETE-> Método "Deletar um jogo que não existe no banco de dados', async () => {
  
    const id_jogo = 1000;
    await axios.delete(`http://localhost:5000/jogos/${id_jogo}`).catch(
        function(error){
            if (error.response){
                expect(error.response.status).toBe(404);

            }
        });

});

//----------------------------------------------------------------------------------------------------------

test('PUT-> Método "Edita o nome de um jogo para RE4" ', async ()=>{
    const id_jogo = 1;
    let jogo = 
    {
        "nome_jogo": "RE4",
    }

    const response =
    await axios.put(`http://localhost:5000/jogos/${id_jogo}`, jogo);
    expect(response.status).toBe(200);
    expect(response.data).toHaveProperty('message','Jogo atualizado com sucesso');


});

//----------------------------------------------------------------------------------------------------------

test('PUT-> Método "Edita a plataforma de um jogo para PC" ', async ()=>{
    const id_jogo = 1;
    let jogo = 
    {
        "plataforma_jogo": "PC",
    }

    const response =
    await axios.put(`http://localhost:5000/jogos/${id_jogo}`, jogo);
    expect(response.status).toBe(200);
    expect(response.data).toHaveProperty('message','Jogo atualizado com sucesso');


});

//----------------------------------------------------------------------------------------------------------

