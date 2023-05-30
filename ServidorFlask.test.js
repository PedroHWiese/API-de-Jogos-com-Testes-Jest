const axios = require('axios');



//----------------------------------------------------------------------------------------------------------
test('POST -> Método "Cria um jogo com o nome GTA" ', async ()=>{
    //Preparar o cenário
    let jogo = 
    {
        "nome_jogo": "GTA",
        "plataforma_jogo": "PS2"
    }

    const response =
    await axios.post('http://localhost:5000/jogos', jogo);
    expect(response.status).toBe(201);
    expect(response.data).toHaveProperty('message','Jogo GTA criado com sucesso');

});

//----------------------------------------------------------------------------------------------------------
test('POST -> Método "Cria um jogo com nome de caracteres além do limite" ', async ()=>{
    //Preparar o cenário
    let jogo = 
    {
        "nome_jogo": "XD".repeat(46),
        "plataforma_jogo": "PS2"
    }

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
    const id_jogo = 6;
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
    const id_jogo = 1000;
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
    const id_jogo = 6;
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
    const id_jogo = 6;
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